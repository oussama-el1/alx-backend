import { createClient, print } from 'redis';

const client = createClient();

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client
  .MULTI()
  .hset('HolbertonSchools', 'Portland', 50, print)
  .hset('HolbertonSchools', 'Seattle', 80, print)
  .hset('HolbertonSchools', 'New York', 20, print)
  .hset('HolbertonSchools', 'Bogota', 20, print)
  .hset('HolbertonSchools', 'Cali', 40, print)
  .hset('HolbertonSchools', 'Paris', 2, print)
  .EXEC();

client.hgetall('HolbertonSchools', (err, data) => {
  console.log(data);
});
