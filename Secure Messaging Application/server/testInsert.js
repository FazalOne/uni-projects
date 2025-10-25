require('dotenv').config();
const mongoose = require('mongoose');
const Message = require('./server/models/message.model');

const ATLAS_URI = process.env.ATLAS_URI || 'your connection string here';

async function run() {
  try {
    await mongoose.connect(ATLAS_URI);
    console.log('Connected to MongoDB');

    const testMessage = new Message({
      sender: new mongoose.Types.ObjectId(),
      recipient: new mongoose.Types.ObjectId(),
      iv: 'testiv',
      message: 'Test encrypted message',
      key: 'testkey',
      signature: 'testsignature',
      publicKey: 'testpublickey'
    });

    const saved = await testMessage.save();
    console.log('Message saved:', saved);

    await mongoose.disconnect();
  } catch (err) {
    console.error(err);
  }
}

run();
