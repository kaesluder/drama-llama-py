import { useState } from 'react';
import { PropTypes } from 'prop-types';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function DialogAddFeed(props) {
  const [feedURL, setFeedURL] = useState('');
  const handleChange = function (event) {
    setFeedURL(event.target.value);
  };

  const handleSubmit = function (event) {
    // pass up feedURL
    props.handleAddFeed(feedURL);
    setFeedURL('');
    props.toggleAddFeedOpen();
  };

  return (
    <div>
      <Dialog open={props.open}>
        <DialogTitle>Subscribe</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Add the url of a feed you wish to subscribe to.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="feedURL"
            label="Feed URL"
            type="url"
            fullWidth
            variant="standard"
            value={feedURL}
            onChange={handleChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={props.toggleAddFeedOpen}>Cancel</Button>
          <Button onClick={handleSubmit}>Add Feed</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

DialogAddFeed.propTypes = {
  handleAddFeed: PropTypes.func,
  toggleAddFeedOpen: PropTypes.func,
};
