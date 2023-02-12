import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import BeenhereIcon from '@mui/icons-material/Beenhere';
import ArticleIcon from '@mui/icons-material/Article';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import * as DOMPurify from 'dompurify';
import * as R from 'ramda';
import { DateTime } from 'luxon';
import './Item.css';

/**
 * Renders a single item.
 * @param {Object} props
 * @returns {JSX.Element} rendered item
 */
const Item = function (props) {
  /**
   * Convert an parsed unix timestamp into a locale string.
   * @param {int} parsedDate
   * @returns {string} locale-formatted date string.
   */
  const convertParsedDate = (parsedDate) =>
    DateTime.fromSeconds(parsedDate).toLocaleString();

  const chipLabel = (result) => (
    <Chip label={result['tag']} key={result['tag']}></Chip>
  );

  // list of tags for each item
  const tagList = R.pipe(
    R.filter(R.prop('result')),
    R.map(chipLabel)
  )(props.itemData['filter_results']);

  // style used for read items
  const readStyle = props.itemData['dl_read'] ? { color: 'text.disabled' } : {};

  // sanitized version of summary
  const clean_summary = DOMPurify.sanitize(
    props.itemData['summary'] ?? 'no summary'
  );

  const readIcon = function () {
    if (props.itemData['dl_read']) {
      return <BeenhereIcon sx={{ mr: 1 }} />;
    } else {
      return <ArticleIcon sx={{ mr: 1 }} />;
    }
  };

  // formatted author line if author is present, empty string otherwise
  const formattedAuthor = props.itemData['author']
    ? `Author: ${props.itemData['author']}`
    : '';

  return (
    <Paper sx={{ m: 1 }}>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
          sx={readStyle}
        >
          {readIcon()}
          <Stack>
            <div>
              <Typography>{props.itemData['title'] ?? 'no title'}</Typography>
            </div>
            <div>
              <Chip
                label={convertParsedDate(props.itemData['published_parsed'])}
              ></Chip>
              {tagList}
            </div>
            <Divider variant="inset" sx={{ m: 1 }} />
            <div>
              <Link
                href={props.itemData['link'] ?? ''}
                target="_blank"
                rel="noreferrer"
              >
                {new URL(props.itemData['link'] ?? '').hostname}
              </Link>
            </div>
            <div>{formattedAuthor}</div>
          </Stack>
        </AccordionSummary>
        <AccordionDetails>
          <Box>
            <div
              sx={{ width: 1 }}
              className="itemSummary"
              dangerouslySetInnerHTML={{ __html: clean_summary }}
            />
          </Box>
        </AccordionDetails>
      </Accordion>
    </Paper>
  );
};

export default Item;

Item.propTypes = {
  itemData: PropTypes.object,
};
