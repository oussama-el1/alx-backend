/* eslint-disable jest/no-test-callback */
/* eslint-disable prefer-arrow-callback */
/* eslint-disable prefer-destructuring */
/* eslint-disable no-unused-expressions */
/* eslint-disable jest/prefer-expect-assertions */
/* eslint-disable jest/valid-expect */
import { createQueue } from 'kue';
import chai from 'chai';
import sinon from 'sinon';
import createPushNotificationsJobs from './8-job';

const { expect } = chai;
const queue = createQueue();
const jobs = [
  {
    phoneNumber: '+21215414141',
    message: 'This is the code 5579 to verify your account',
  },
];

describe('createPushNotificationsJobs', () => {
  // eslint-disable-next-line jest/no-hooks
  beforeEach(() => {
    sinon.spy(console, 'log');
  });

  // eslint-disable-next-line no-undef
  before(() => {
    queue.testMode.enter();
  });

  // eslint-disable-next-line jest/no-hooks
  afterEach(() => {
    sinon.restore();
    queue.testMode.clear();
  });

  // eslint-disable-next-line no-undef
  after(() => {
    queue.testMode.exit();
  });

  it('display a error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(1, queue)).to.throw();
  });

  it('throws if queue is not a valid kue', () => {
    expect(() => createPushNotificationsJobs(jobs, '')).to.throw();
  });

  it('test the creation of jobs', () => {
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(1);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql(jobs[0]);
    expect(console.log.calledOnceWith(`Notification job created: ${queue.testMode.jobs[0].id}`)).to.be.true;
  });

  it('test job progress event report', (done) => {
    createPushNotificationsJobs(jobs, queue);
    queue.testMode.jobs[0].addListener('progress', () => {
      const id = queue.testMode.jobs[0].id;
      expect(console.log.calledWith(`Notification job ${id} 50% complete`)).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('progress', 50, 100);
  });

  it('test job failed event report', (done) => {
    createPushNotificationsJobs(jobs, queue);
    queue.testMode.jobs[0].addListener('failed', () => {
      const id = queue.testMode.jobs[0].id;
      expect(console.log.calledWith(`Notification job ${id} failed: job failed!`)).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('failed', new Error('job failed!'));
  });

  it('test job completed event report', (done) => {
    createPushNotificationsJobs(jobs, queue);
    queue.testMode.jobs[0].addListener('complete', () => {
      const id = queue.testMode.jobs[0].id;
      expect(console.log.calledWith(`Notification job ${id} completed`)).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('complete', true);
  });
});
