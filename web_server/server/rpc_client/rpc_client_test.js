const client = require('./rpc_client');

client.add(1, 2, (response) => {
  console.assert(response === 3);
});

client.getNewsSummariesForUser('test_user', 2, (response) => {
  console.assert(response != null);
});

client.logNewsClickForUser('test_user', 'test_news');
