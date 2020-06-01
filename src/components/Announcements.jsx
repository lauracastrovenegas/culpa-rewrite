import PropTypes from 'prop-types';
import React from 'react';

import ErrorComponent from 'components/common/ErrorComponent';
import LoadingComponent from 'components/common/LoadingComponent';
import useDataFetch from 'components/common/useDataFetch';

const propTypes = {
  messages: PropTypes.arrayOf(PropTypes.string).isRequired,
};

function AnnouncementsSection(props) {
  // TODO: Implement Announcements
  const { messages } = props;
  return <div>{messages}</div>;
}

AnnouncementsSection.propTypes = propTypes;

export default function Announcements() {
  const {
    data: { messages },
    isLoading,
    isError,
  } = useDataFetch('/api/announcements/', {
    messages: [],
  });

  if (isLoading || isError) {
    return isLoading ? <LoadingComponent /> : <ErrorComponent />;
  }

  return <AnnouncementsSection messages={messages} />;
}
