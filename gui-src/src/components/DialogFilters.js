import { useState } from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import * as R from 'ramda';

export default function DialogFilters(props) {
  // TODO: Tooltips and figure out what I'm going to do with filter type.
  // USABILITY: Yeeeeeeesh. Barely functional.

  const [selectedIndex, setSelectedIndex] = useState();

  const kDefaultFields = {
    id: '',
    tag: '',
    message: '',
    explanation: '',
    regex: '',
    type: 'RegexFilter',
  };

  const [errorState, setErrorState] = useState({});
  const [submitDisabled, setSubmitDisabled] = useState(true);
  const [formData, setFormData] = useState(kDefaultFields);

  /**
   * Returns true if regStr is a valid regular expression.
   * @param {string} regStr
   * @returns
   */
  const validateRegex = function (regStr) {
    try {
      new RegExp(regStr);
      return true;
    } catch {
      return false;
    }
  };

  /**
   * Check that all required values are present before
   * trying to submit.
   * @returns
   */
  const preSubmitValidate = function () {
    for (let field in validateFields) {
      if (!validateFields[field](formData[field])) {
        return false;
      }
    }
    return true;
  };

  /**
   * Object for connecting field-names to validation functions.
   * Each validation function should return a bool.
   */
  const validateFields = {
    type: (v) => R.find(R.equals(v))(['RegexFilter', 'BaseFilter']),
    id: (v) => v.length > 3,
    tag: (v) => v.length > 0,
    regex: (v) => validateRegex(v),
  };

  /**
   * Object for storing helper texts for each field.
   */
  const helperTexts = {
    type: 'Only RegexFilter and BaseFilter are supported.',
    id: 'ID must be longer than 3 characters.',
    tag: "Tag can't be empty.",
    regex: 'Must be a valid regular expression.',
  };

  /**
   * Handles selection of list items from the menu. Changes
   * form values to data from filter spec in filterList.
   * @param {event} event
   * @param {string} index
   */
  const handleListItemClick = function (event, index) {
    if (selectedIndex === index) {
      setSelectedIndex(null);
      setFormData(kDefaultFields);
    } else {
      setSelectedIndex(index);

      // set FormData to the data for the selected filter
      setFormData(
        R.mergeDeepRight(
          kDefaultFields,
          R.find(R.propEq('id', index))(props.filterList)
        )
      );
    }
  };

  /** render the list items if filterList has been passed
   * from the database.
   */
  let listItems = null;

  if (props.filterList) {
    listItems = props.filterList.map((filterSpec) => {
      return (
        <ListItemButton
          selected={selectedIndex === filterSpec['id']}
          onClick={(event) => handleListItemClick(event, filterSpec['id'])}
          key={filterSpec['id']}
        >
          <ListItemText>
            `{filterSpec['id']} : {filterSpec['tag']}`
          </ListItemText>
        </ListItemButton>
      );
    });
  }

  /**
   * Builds a single input field using fieldName.
   * @param {fieldName} fieldName
   * @returns
   */
  const buildField = function (fieldName) {
    return (
      <div key={fieldName}>
        <TextField
          helperText={helperTexts[fieldName]}
          error={errorState[fieldName]}
          sx={{ m: 0.5 }}
          id={fieldName}
          label={fieldName}
          key={fieldName}
          value={formData[fieldName]}
          variant="outlined"
          onChange={handleChange}
        />
      </div>
    );
  };

  /** TODO consolidate this with the other validation
   * function.
   */
  const missingFormData = function () {
    for (let key in validateFields) {
      if (!validateFields[key](formData[key])) {
        return true;
      }
    }

    return false;
  };

  /**
   * Handles change events in text fields.
   * @param {event} event
   */
  const handleChange = function (event) {
    const id = event.target.id;
    const value = event.target.value;

    setFormData(R.assoc(id, value));
    if (validateFields[id]) {
      setErrorState(R.assoc(id, !Boolean(validateFields[id](value))));
      setSubmitDisabled(!Boolean(validateFields[id](value)));
    }

    if (missingFormData()) {
      setSubmitDisabled(true);
    } else {
      setSubmitDisabled(false);
    }

    console.log(missingFormData());
  };

  /**
   * Reset form fields when cancel is selected.
   * @param {Event} event
   */
  const handleCancel = function (event) {
    setFormData(kDefaultFields);
    props.toggleFilterDialogOpen();
  };

  /**
   * Pass formData up to create a filter.
   * @param {event} event
   */
  const handleSubmit = function (event) {
    if (preSubmitValidate()) {
      props.handleAddFilter(formData);
      handleCancel();
    }
  };

  const formFields = R.map(buildField)(R.keys(formData));

  return (
    <Dialog open={props.filterDialogOpen} fullWidth={true} maxWidth="md">
      <DialogTitle>Add or Edit Forms</DialogTitle>
      <DialogContent>
        <Grid container spacing={1}>
          <Grid item xs={3}>
            <List>{listItems}</List>
          </Grid>
          <Grid item xs={9}>
            {formFields}
            <Button onClick={handleCancel}>Cancel</Button>
            <Button disabled={submitDisabled} onClick={handleSubmit}>
              Submit
            </Button>
          </Grid>
        </Grid>
      </DialogContent>
    </Dialog>
  );
}

DialogFilters.propTypes = {
  filterList: PropTypes.array,
  toggleFilterDialogOpen: PropTypes.func,
  handleAddFilter: PropTypes.func,
};
