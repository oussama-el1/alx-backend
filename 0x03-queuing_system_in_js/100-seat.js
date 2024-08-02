import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
import express from 'express';

let reservationEnabled;
const client = createClient();

const reserveSeat = (number) => client.SET('available_seats', number);

const getCurrentAvailableSeats = async () => {
  const getAsync = promisify(client.get).bind(client);

  try {
    const seats = await getAsync('available_seats');
    return parseInt(seats, 10);
  } catch (err) {
    throw new Error(err.message);
  }
};

const queue = createQueue();
const app = express();
const PORT = 1245;

app.get('/available_seats', async (req, res) => {
  try {
    const data = await getCurrentAvailableSeats();
    res.statusCode = 200;
    res.json({ available_seats: data });
  } catch (err) {
    res.json({ status: err.message });
  }
});

app.get('/reserve_seat', (req, res) => { /* eslint-disable-line consistent-return */
  if (reservationEnabled === false) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.createJob('reserve_seat')
    .save((err) => {
      if (!err) res.json({ status: 'Reservation in process' });
      else res.json({ status: 'Reservation failed' });
    });
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message || err.toString()}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    let availableSeats = await getCurrentAvailableSeats();
    availableSeats -= 1;
    reserveSeat(availableSeats);
    if (availableSeats >= 0) {
      if (availableSeats === 0) reservationEnabled = false;
      done();
    }
    done(new Error('Not enough seats available'));
  });
});

app.listen(PORT, () => {
  reserveSeat(50);
  reservationEnabled = true;
  console.log(`server listning on ${PORT}...`);
});

client.on('connect', async () => {
  console.log('Connected to Redis...');
});

client.on('error', (err) => {
  console.error('Redis error:', err);
});
