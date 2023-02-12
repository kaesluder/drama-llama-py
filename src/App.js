import { useEffect, useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import BeenhereIcon from '@mui/icons-material/Beenhere';
import MenuIcon from '@mui/icons-material/Menu';
import RefreshIcon from '@mui/icons-material/Refresh';
import LibraryAddIcon from '@mui/icons-material/LibraryAdd';
import Grid from '@mui/material/Grid';
import { useSnackbar } from 'notistack';
import FilterListIcon from '@mui/icons-material/FilterList';
import './App.css';

import {
  getFeedData,
  getEntriesForFeed,
  requestRefresh,
  markFeedRead,
  addFeed,
  preDeleteFeed,
  deleteFeed,
  getFilters,
  addFilter,
} from './LlamaAPI';

import FeedList from './components/FeedList';
import ItemList from './components/ItemList';
import DialogAddFeed from './components/DialogAddFeed';
import DialogPreDelete from './components/DialogPreDelete';
import DialogFilters from './components/DialogFilters';

function App() {
  const [feedsStatus, setFeedsStatus] = useState([]);
  const [itemsStatus, setItemsStatus] = useState([]);
  const [selectedFeedStatus, setSelectedFeedStatus] = useState();
  const [addFeedOpen, setAddFeedOpen] = useState(false);
  const [deleteFeedOpen, setDeleteFeedOpen] = useState(false);
  const [deleteFeedID, setDeleteFeedID] = useState();
  const [deleteCount, setDeleteCount] = useState();
  const [filterDialogOpen, setFilterDialogOpen] = useState(false);
  const [filterList, setFilterList] = useState();
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const handleFeedSelect = function (feedID) {
    setSelectedFeedStatus(feedID);
    console.log(`handleFeedSelect ${feedID}`);
    return getEntriesForFeed(feedID)
      .then((response) => setItemsStatus(response.data))
      .catch((error) =>
        enqueueSnackbar(`Error fetching items for ${feedID}: ${error.response}`)
      );
  };

  const handleAddFeed = function (sourceURL) {
    return addFeed(sourceURL)
      .then((response) => {
        return getFeedData();
      })
      .then((response) => {
        return setFeedsStatus(response.data);
      })
      .catch((error) => {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
          enqueueSnackbar(
            `Error fetching feed from: ${sourceURL}. Error: ${error.response.data.exception}`,
            { variant: 'warning' }
          );
        }
      });
  };

  const handleAddFilter = function (formData) {
    console.log(`handleAddFilter: ${JSON.stringify(formData)}`);
    return addFilter(formData)
      .then((response) => setFilterList(response.data))
      .catch((error) =>
        enqueueSnackbar(`Error fetching filters: ${error.response}`)
      );
  };

  const handleRefresh = function (event) {
    console.log('handleRefresh');
    return requestRefresh()
      .then((response) => {
        console.log('getFeedData');
        return getFeedData();
      })
      .then((response) => {
        console.log('setFeedsStatus');
        return setFeedsStatus(response.data);
      })
      .then(() => {
        console.log('getEntriesForFeed');
        return getEntriesForFeed(selectedFeedStatus);
      })
      .then((response) => {
        console.log('setItemsStatus');
        setItemsStatus(response.data);
      })
      .catch((error) =>
        enqueueSnackbar(`Error refreshing feeds: ${error.response}`)
      );
  };

  const handleMarkFeedRead = function (event) {
    console.log('handleMarkFeedRead');
    return markFeedRead(selectedFeedStatus).then((response) =>
      setItemsStatus(response.data)
    );
  };

  const handlePreDelete = function (feed_id) {
    console.log(`handlePreDelete ${feed_id}`);
    return preDeleteFeed(feed_id)
      .then((response) => {
        setDeleteCount(response.data['item_count']);
        setDeleteFeedID(feed_id);
        toggleDeleteFeedOpen();
      })
      .catch((error) =>
        enqueueSnackbar(`Error with pre-delete: ${error.response}`)
      );
  };

  const handleDelete = function (feed_id) {
    console.log(`handleDelete ${feed_id}`);
    return deleteFeed(feed_id)
      .then((response) => setFeedsStatus(response.data))
      .catch((error) =>
        enqueueSnackbar(`Error with pre-delete: ${error.response}`)
      );
  };

  // REFACTOR
  const toggleAddFeedOpen = function (event) {
    setAddFeedOpen((curr) => !curr);
  };

  const toggleDeleteFeedOpen = function (event) {
    setDeleteFeedOpen((curr) => !curr);
  };

  const toggleFilterDialogOpen = function (event) {
    setFilterDialogOpen((curr) => !curr);
  };

  useEffect(() => {
    getFeedData()
      .then((response) => {
        setFeedsStatus(response.data);
      })
      .then(() => getFilters())
      .then((response) => setFilterList(response.data))
      .catch((error) =>
        enqueueSnackbar(`Error fetching feeds: ${error.response}`)
      );
  }, [enqueueSnackbar]);

  return (
    <div className="App">
      <header className="App-header">
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="menu"
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="refresh"
                sx={{ mr: 2 }}
                onClick={handleRefresh}
              >
                <RefreshIcon /> <Typography>Refresh</Typography>
              </IconButton>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="refresh"
                sx={{ mr: 2 }}
                onClick={handleMarkFeedRead}
              >
                <BeenhereIcon />
                <Typography>Mark Read</Typography>
              </IconButton>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="refresh"
                sx={{ mr: 2 }}
                onClick={toggleAddFeedOpen}
              >
                <LibraryAddIcon />
                <Typography>Add Feed</Typography>
              </IconButton>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="refresh"
                sx={{ mr: 2 }}
                onClick={toggleFilterDialogOpen}
              >
                <FilterListIcon />
                <Typography>Add/Edit Filters</Typography>
              </IconButton>
            </Toolbar>
          </AppBar>
          <Grid container spacing={1}>
            <Grid item xs={3}>
              <Box>
                <FeedList
                  feedsStatus={feedsStatus}
                  handleFeedSelect={handleFeedSelect}
                  handlePreDelete={handlePreDelete}
                ></FeedList>
              </Box>
            </Grid>
            <Grid item xs={9}>
              <div className={'articles'}>
                <ItemList itemsStatus={itemsStatus}></ItemList>
              </div>
            </Grid>
          </Grid>
          <DialogAddFeed
            open={addFeedOpen}
            toggleAddFeedOpen={toggleAddFeedOpen}
            handleAddFeed={handleAddFeed}
          />
          <DialogPreDelete
            open={deleteFeedOpen}
            toggleDeleteFeedOpen={toggleDeleteFeedOpen}
            deleteFeedID={deleteFeedID}
            deleteCount={deleteCount}
            handleDelete={handleDelete}
          />
          <DialogFilters
            filterDialogOpen={filterDialogOpen}
            filterList={filterList}
            handleAddFilter={handleAddFilter}
            toggleFilterDialogOpen={toggleFilterDialogOpen}
          ></DialogFilters>
        </Box>
      </header>
    </div>
  );
}

export default App;
