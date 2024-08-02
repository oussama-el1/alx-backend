const createPushNotificationsJobs = (jobs, queue) => {
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  }

  for (let job of jobs) {
    job = queue.create('push_notification_code_3', job)
      .save((err) => {
        if (!err) console.log(`Notification job created: ${job.id}`);
      });

    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    job.on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err.toString() || err.message}`);
    });

    job.on('progress', (percentage) => {
      console.log(`Notification job ${job.id} ${percentage}% complete`);
    });
  }
};

module.exports = createPushNotificationsJobs;
