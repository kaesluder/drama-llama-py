import * as React from 'react';
import PropTypes from 'prop-types';
import DeleteIcon from '@mui/icons-material/Delete';
import Tooltip from '@mui/material/Tooltip';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import RssFeed from '@mui/icons-material/RssFeed';

/**
 * React component for handling individual Feeds.
 * @param {Object} props
 *
 * @property {Object} feed  item data object
 * @property {function} handlePreDelete  handler for starting the pre-delete process
 * @property {function} handleSelect  handler for selecting a feed.
 *
 * @returns React component
 */
const FeedItem = function (props) {
  const handleDeleteClick = function (e) {
    props.handlePreDelete(props.feed['dl_feed_id']);
  };

  return (
    <div>
      <ListItem disablePadding>
        <ListItemButton
          onClick={(e) => props.handleSelect(props.feed['dl_feed_id'])}
        >
          <ListItemIcon>
            <RssFeed />
          </ListItemIcon>
          <ListItemText primary={props.feed['title']} />
        </ListItemButton>
        <Tooltip title="remove feed">
          <DeleteIcon
            color="secondary"
            fontSize="small"
            onClick={handleDeleteClick}
          />
        </Tooltip>
      </ListItem>
    </div>
  );
};

/**
 * React component for rendering list of feeds.
 *
 * @param {Object} props
 * @property feedsStatus: List of feeds.
 *
 * @returns react component
 */
const FeedList = function (props) {
  const feeds = props.feedsStatus.map((f) => {
    return (
      <FeedItem
        feed={f}
        handleSelect={props.handleFeedSelect}
        handlePreDelete={props.handlePreDelete}
        key={f.dl_feed_id}
      ></FeedItem>
    );
  });

  return <List>{feeds}</List>;
};

FeedList.propTypes = {
  handlePreDelete: PropTypes.func,
  handleSelect: PropTypes.func,
  feedsStatus: PropTypes.array,
};

ListItem.propTypes = {
  handleSelect: PropTypes.func,
  feed: PropTypes.object,
};

export default FeedList;
