const express = require('express');
const router = express.Router();
const winston = require('winston');
const rpc_client = require('../rpc_client/rpc_client');
const metricsClient = require('../metrics_client/metrics_client');

router.get('/userId/:userId/pageNum/:pageNum', (req, res) => {
  console.log('Fetching news...');
  const user_id = req.params['userId'];
  const page_num = req.params['pageNum'];

  rpc_client.getNewsSummariesForUser(user_id, page_num, function(news) {
    res.json(news);
  });

  metricsClient.increment('coconut_news.web_server.fetch_news');
});

/* Log news click. */
router.post('/userId/:userId/newsId/:newsId', (req,res) => {
  console.log('Logging news click...');
  const user_id = req.params['userId'];
  const news_id = req.params['newsId'];

  rpc_client.logNewsClickForUser(user_id, news_id);
  res.status(200);

  winston.info(`web_server logNewsClickForUser: ${req.connection.remoteAddress}`);
  metricsClient.increment('coconut_news.web_server.user_click_new');
});

module.exports = router;
