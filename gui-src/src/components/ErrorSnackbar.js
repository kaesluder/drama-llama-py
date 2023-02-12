import * as React from 'react';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

export default function SimpleSnackbar(props) {
  const [open, setOpen] = React.useState(false);

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };

  React.useEffect(() => {
    if (props.errorStatus) {
      setOpen(true);
      setTimeout(props.clearError, 6000);
    }
  }, [props.errorStatus, props.clearError]);

  return (
    <div>
      <Snackbar
        open={Boolean(props.errorStatus)}
        autoHideDuration={6000}
        onClose={handleClose}
        message={props.errorStatus}
      />
    </div>
  );
}
