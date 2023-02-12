import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Item from './Item';
import * as R from 'ramda';
import { useEffect } from 'react';

const sortByDate = R.compose(R.reverse, R.sortBy(R.prop('published_parsed')));

/**
 * Render a list of items.
 * @param {Object} props
 * @returns {JSX.Element} Rendered list
 */
const ItemList = function (props) {
  useEffect(() => {
    /* Unorthodox for React, but ensure that clicked links open 
  in a browser window rather than the app window.
  Recipe from: https://www.geeksforgeeks.org/how-to-simulate-target_blank-in-javascript/ */
    document.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && !e.target.hasAttribute('target')) {
        e.target.setAttribute('target', '_blank');
      }
    });
  }, []);

  const renderedList = sortByDate(props.itemsStatus).map((item) => {
    return <Item itemData={item} key={item.id}></Item>;
  });

  return (
    <Box sx={{ height: 'max-content', overflow: 'auto' }}>{renderedList}</Box>
  );
};

ItemList.propTypes = {
  itemsStatus: PropTypes.array,
};

export default ItemList;
