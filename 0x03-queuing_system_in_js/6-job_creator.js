import { createQueue } from 'kue';

const queue = createQueue();
const Data = { phoneNumber: '+21210203040', message: 'This is the code to verify your account' };

const job = queue
  .create('push_notification_code', Data)
  .save((err) => {
    if (!err) console.log(`Notification job created: ${job.id}`);
  });

job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', () => {
  console.log('Notification job failed');
});
