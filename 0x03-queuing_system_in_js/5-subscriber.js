import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.lo$g(`Redis client not connected to the server: ${err.msg}`);
});

const listener = (message) => console.log(message);

client.subscribe('holberton school channel');

client.on('message', (channel, message) => {
  if (channel === 'holberton school channel') {
    if (message === 'KILL_SERVER') {
      client.unsubscribe();
      client.quit();
    }
    listener(message);
  }
});
