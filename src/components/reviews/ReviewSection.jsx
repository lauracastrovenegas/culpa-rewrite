import PropTypes from "prop-types";
import React, { useEffect, useReducer } from "react"
import { Container, Dropdown, Grid, Button, Icon } from "semantic-ui-react"

import ErrorComponent from "components/common/ErrorComponent";
import LoadingComponent from "components/common/LoadingComponent";
import ReviewCard from "components/reviews/ReviewCard"

export default function ReviewSection({initReviews, pageType, id, assocList}){
    const NUM_REVIEWS_PER_PAGE = 3
    const reducer = (state, action) => {
        switch(action.type){
            case "RELOAD_START":
                return {
                    ...state,
                    reload: true
                };
            case "RELOAD_END":
                return {
                    ...state,
                    reload: false
                };
            case "FETCH_START":
                return {
                    ...state,
                    isLoading: true,
                    isError: false
                };
            case "FETCH_SUCCESS":
                return {
                    ...state,
                    isLoading: false,
                    isError: false,
                    reviews: action.payload.reviews
                };
            case "FETCH_FAILURE":
                return {
                    ...state,
                    isLoading: false,
                    isError: true,
                }
            case "CHANGE_SORTING":
                return {
                    ...state,
                    pag_num: 1,
                    sorting: action.payload.sorting
                };
            case "CHANGE_FILTER_YEAR":
                return {
                    ...state,
                    pag_num: 1,
                    filters: {
                        assocListLimit: state.filters.assocListLimit,
                        year: action.payload.filterYear,
                        yearText: action.payload.filterYearText
                    }
                }
            case "CHANGE_FILTER_ASSOC_LIST":
                return {
                    ...state,
                    pag_num: 1,
                    filters: {
                        ...state.filters,
                        assocListLimit: action.payload.assocListLimit
                    }
                }
            case "INCREMENT_PAG_NUM":
                return {
                    ...state,
                    pag_num: state.pag_num + 1
                }
            default:
                throw new Error()
        }
    }
    const [state, dispatch] = useReducer(reducer, {
        reload: false,
        isLoading: false,
        isError: false,
        pag_num: 1,
        reviews: initReviews,
        assocList,
        pageType,
        id,
        sorting: '',
        filters: {
            assocListLimit: [],
            year: null,
            yearText: '',
        }
    })

    const fetchReviews = async () => {
        dispatch({type: 'FETCH_START'})
        const filterList = state.filters.assocListLimit.join(',')
        const res = await fetch(
            `/api/review/get/${state.pageType}/${state.id}`
            + `?sorting=${state.sorting}`
            + `&filterList=${filterList}`
            + `&filterYear=${state.filters.year}`, 
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
            },
        })
        try {
            const result = await res.json()
            if (!res.ok){
                dispatch({type: "FETCH_FAILURE", payload: result.error})
            } else {
                dispatch({type: "FETCH_SUCCESS", payload: result})
            }
            return result

        } catch(error){
            dispatch({type: "FETCH_FAILURE", payload: error})
            return {'error': error}
        }
    }

    useEffect(() => {
        if(state.reload){
            fetchReviews()
            dispatch({type: "RELOAD_END"})
        }
    })

    if (state.isLoading || state.isError) {
        return state.isLoading ? <LoadingComponent /> : <ErrorComponent />;
    }

    const sortingOptions = [
        {key: 0, text: 'None', value: ''},
        {key: 1, text: 'Most Positive', value: 'Most Positive'},
        {key: 2, text: 'Most Negative', value: 'Most Negative'},
        {key: 3, text: 'Newest', value: 'Newest'},
        {key: 4, text: 'Oldest', value: 'Oldest'},
        {key: 5, text: 'Most Agreed', value: 'Most Agreed'},
        {key: 6, text: 'Most Disagreed', value: 'Most Disagreed'}
    ]

    const onSortChange = (e, data) => {
        dispatch({type: "RELOAD_START"})
        dispatch({type: 'CHANGE_SORTING', payload: {sorting: data.value}})
    }

    const filterYearOptions = [
        {key: 0, text: 'None', value: null},
        {key: 1, text: 'Written within 2 years', value: 2},
        {key: 2, text: 'Written within 5 years', value: 5}
    ]

    const onFilterYearChange = (e, data) => {
        dispatch({type: "RELOAD_START"})
        dispatch({type: 'CHANGE_FILTER_YEAR', payload: {
            filterYear: data.value,
            filterYearText: data.text
        }})
    }

    const filterAssocListOptions = state.assocList.map((item) => {
        const oType = state.pageType === 'professor' ? 'course' : 'professor'
        return ({
            key: item[`${oType}Id`],
            value: item[`${oType}Id`],
            text: oType === 'professor' ? 
                `${item.firstName} ${item.lastName}` :
                `[${item.courseCode}] ${item.courseName}`
        })
    })

    const onFilterAssocListChange = (e, data) => {
        dispatch({type: "RELOAD_START"})
        dispatch({
            type: "CHANGE_FILTER_ASSOC_LIST",
            payload: {
                assocListLimit: data.value
            }
        })
    }

    const onClickPagButton = () => {
        dispatch({type: "INCREMENT_PAG_NUM"})
    }

    return (
        <Container fluid>
            <Grid>
                <Grid.Row key={1}>
                    <Grid.Column key={1} width={4}>
                        <Dropdown 
                            fluid
                            selection
                            name="sortingDropdown"
                            options={sortingOptions}
                            placeholder="Sort by"
                            text={state.sorting}
                            value={state.sorting}
                            onChange={onSortChange}
                        />
                    </Grid.Column>
                    <Grid.Column key={2} width={4}>
                        <Dropdown 
                                fluid
                                selection
                                name="filteringSingleSelectDropdown"
                                options={filterYearOptions}
                                placeholder="Filter by"
                                text={state.filters.yearText}
                                value={state.filters.year}
                                onChange={onFilterYearChange}
                            />
                    </Grid.Column>
                    <Grid.Column key={3} width={1} />
                    <Grid.Column key={4} width={7}>
                        <Dropdown
                            fluid
                            multiple
                            search
                            selection
                            name="filteringMultiSelectDropdown"
                            options={filterAssocListOptions}
                            placeholder={state.pageType === 'professor' ?
                                'Search for a specific course' : 
                                'Search for a specific professor'
                            }
                            value={state.filters.assocListLimit}
                            onChange={onFilterAssocListChange}
                        />
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row key={2}>
                    {state.reviews.slice(
                        0, state.pag_num * NUM_REVIEWS_PER_PAGE
                    ).map((review) => {return (
                        <ReviewCard 
                            content={review.content}
                            deprecated={review.deprecated}
                            key={review.reviewId}
                            reviewHeader={review.reviewHeader}
                            reviewId={review.reviewId}
                            reviewType={review.reviewType}
                            submissionDate={review.submissionDate}
                            votes={review.votes}
                            workload={review.workload}
                        />
                    )})}
                </Grid.Row>
                <Grid.Row centered key={3} style={{marginBottom: '50px'}}>
                    <Button fluid size='large' onClick={onClickPagButton}>
                        Show more<Icon name="arrow down" style={{marginLeft: '5px'}}/>
                    </Button>
                </Grid.Row>
            </Grid>
            
        </Container>
    )
}

const propTypes = {
    initReviews: PropTypes.arrayOf(
        PropTypes.shape({
            reviewType: PropTypes.oneOf(['professor', 'course']).isRequired,
            reviewHeader: PropTypes.oneOfType([
                PropTypes.shape({
                    courseId: PropTypes.number.isRequired,
                    courseName: PropTypes.string.isRequired,
                    courseCode: PropTypes.string.isRequired,
                }),
                PropTypes.shape({
                    profId: PropTypes.number.isRequired,
                    profFirstName: PropTypes.string.isRequired,
                    profLastName: PropTypes.string.isRequired,
                    uni: PropTypes.string.isRequired
                }),
            ]).isRequired,
            votes: PropTypes.shape({
                initUpvoteCount: PropTypes.number.isRequired,
                initDownvoteCount: PropTypes.number.isRequired,
                initFunnyCount: PropTypes.number.isRequired,
                upvoteClicked: PropTypes.bool.isRequired,
                downvoteClicked: PropTypes.bool.isRequired,
                funnyClicked: PropTypes.bool.isRequired,
            }).isRequired,
            workload: PropTypes.string,
            submissionDate: PropTypes.string.isRequired,
            reviewId: PropTypes.number.isRequired,
            deprecated: PropTypes.bool,
            content: PropTypes.string,
        })
    ).isRequired,
    pageType: PropTypes.string.isRequired,
    id: PropTypes.number.isRequired,
    assocList: PropTypes.arrayOf(
        PropTypes.oneOfType([
            PropTypes.shape({
                professorId: PropTypes.number.isRequired,
                firstName: PropTypes.string.isRequired,
                lastName: PropTypes.string.isRequired
            }),
            PropTypes.shape({
                courseId: PropTypes.number.isRequired,
                courseCode: PropTypes.string.isRequired,
                courseName: PropTypes.string.isRequired
            })
        ])
    ).isRequired
}

ReviewSection.propTypes = propTypes