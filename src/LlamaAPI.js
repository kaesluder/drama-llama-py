import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const getFeedData = function () {
  return axios.get(`${API_URL}/feeds`);
};

const getEntriesForFeed = function (feedID) {
  return axios.get(`${API_URL}/${feedID}/entries`);
};

const requestRefresh = function () {
  return axios.get(`${API_URL}/refresh`);
};

const markFeedRead = function (feedID) {
  return axios.patch(`${API_URL}/${feedID}/read`);
};

const addFeed = function (sourceURL) {
  const formData = { feed_source: sourceURL };
  return axios.post(`${API_URL}/feeds/add`, formData);
};

const preDeleteFeed = function (feed_id) {
  return axios.get(`${API_URL}/feeds/${feed_id}/predelete`);
};

const deleteFeed = function (feed_id) {
  return axios.delete(`${API_URL}/feeds/${feed_id}/delete`);
};

const getFilters = function () {
  return axios.get(`${API_URL}/filters`);
};

const addFilter = function (filterSpec) {
  return axios.post(`${API_URL}/filters/add`, filterSpec);
};

export {
  getFeedData,
  getEntriesForFeed,
  requestRefresh,
  markFeedRead,
  addFeed,
  preDeleteFeed,
  deleteFeed,
  getFilters,
  addFilter,
};
