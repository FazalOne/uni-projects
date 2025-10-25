const express = require('express'); 
const router = express.Router();
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json();
const User = require('../models/user.model');
const Message = require('../models/message.model');
const crypto = require('crypto');
const Group = require('../models/group.model');
const forge = require('node-forge');
require('dotenv').config();

const keypair = forge.pki.rsa.generateKeyPair({ bits: 2048 });
const privateKey = keypair.privateKey;
const publicKeyPem = forge.pki.publicKeyToPem(keypair.publicKey);

const encrypt = (message) => {
    const key = crypto.randomBytes(32);
    const iv = crypto.randomBytes(16);
    let cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
    let encrypted = cipher.update(message);
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    return {
        iv: iv.toString('hex'),
        encryptedMessage: encrypted.toString('hex'),
        key: key.toString('hex')
    };
};

const createMessage = async (sender, userToken, recipient, message) => {
    let _info = null;
    const user = await User.findOne({_id: sender, token: userToken});
    if (!user) {
        console.log("User not found or invalid token");
        return null;
    }

    const _user = await User.findOne({email: recipient});
    if (!_user) {
        console.log("Recipient user not found");
        return null;
    }

    if (!_user.communications.includes(sender)) {
        _user.communications.push(sender);
        await _user.save();
        console.log("Added sender to recipient's communications");
    }

    const encryptedMessage = encrypt(message);
    const md = forge.md.sha256.create();
    md.update(encryptedMessage.encryptedMessage, 'utf8');
    const signature = privateKey.sign(md);
    const signatureHex = forge.util.bytesToHex(signature);

    const _message = new Message({
        recipient: _user._id,
        sender,
        iv: encryptedMessage.iv,
        message: encryptedMessage.encryptedMessage,
        key: encryptedMessage.key,
        signature: signatureHex,
        publicKey: publicKeyPem
    });

    console.log("Saving message to DB:", _message);
    try {
        await _message.save();
        console.log("Message saved successfully");
    } catch (err) {
        console.error("Error saving message:", err);
    }

    _info = {
        recipient: {email: _user.email, id: _user._id},
        sender: {email: user.email, id: user._id},
        iv: encryptedMessage.iv,
        message: encryptedMessage.encryptedMessage,
        key: encryptedMessage.key,
        signature: signatureHex,
        publicKey: publicKeyPem
    };

    return _info;
};

const createGroupMessage = async (sender, userToken, groupId, message) => {
    let _info = null;
    const user = await User.findOne({_id: sender, token: userToken});
    if (!user) return null;

    const group = await Group.findOne({_id: groupId});
    if (!group) return null;

    const encryptedMessage = encrypt(message);
    const md = forge.md.sha256.create();
    md.update(encryptedMessage.encryptedMessage, 'utf8');
    const signature = privateKey.sign(md);
    const signatureHex = forge.util.bytesToHex(signature);

    const _message = new Message({
        recipient: group._id,
        sender,
        iv: encryptedMessage.iv,
        message: encryptedMessage.encryptedMessage,
        key: encryptedMessage.key,
        signature: signatureHex,
        publicKey: publicKeyPem
    });

    await _message.save();

    _info = {
        recipient: {id: group._id, member: group.member, code: group.code},
        sender: {email: user.email, id: user._id},
        iv: encryptedMessage.iv,
        message: encryptedMessage.encryptedMessage,
        key: encryptedMessage.key,
        signature: signatureHex,
        publicKey: publicKeyPem
    };

    return _info;
};

const startMessage = async (sender, userToken, recipient) => {
    const user = await User.findOne({_id: sender, token: userToken});
    if (!user) return null;

    const _user = await User.findOne({email: recipient});
    if (!_user) return null;

    if (!user.communications.includes(_user._id) && sender !== recipient) {
        user.communications.push(_user._id);
        try {
            await user.save();
            return true;
        } catch {
            return null;
        }
    }
};

router.post('/get_messages', jsonParser, async (req, res) => {
    const {user, token, target} = req.body;
    const loggedUser = await User.findOne({_id: user, token});
    if (!loggedUser) return res.status(403).json("Permission denied.");

    const targetUser = await User.findOne({email: target});
    if (!targetUser) return res.status(404).json("User not found.");

    try {
        const sentMessages = await Message.find({sender: user, recipient: targetUser._id});
        const receivedMessages = await Message.find({sender: targetUser._id, recipient: user});
        const allMessages = sentMessages.concat(receivedMessages).sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));

        const finalResult = allMessages.map(msg => {
            if (String(msg.sender) === String(loggedUser._id)) {
                return {
                    recipient: {email: targetUser.email, id: targetUser._id},
                    sender: {email: loggedUser.email, id: loggedUser._id},
                    iv: msg.iv,
                    message: msg.message,
                    key: msg.key,
                    signature: msg.signature,
                    publicKey: msg.publicKey
                };
            } else {
                return {
                    recipient: {email: loggedUser.email, id: loggedUser._id},
                    sender: {email: targetUser.email, id: targetUser._id},
                    iv: msg.iv,
                    message: msg.message,
                    key: msg.key,
                    signature: msg.signature,
                    publicKey: msg.publicKey
                };
            }
        });

        res.json(finalResult);
    } catch {
        res.status(500).json("Something went wrong.");
    }
});

router.post('/get_group_messages', jsonParser, async (req, res) => {
    const {user, token, target} = req.body;
    const currentUser = await User.findOne({_id: user, token});
    if (!currentUser) return res.status(403).json("Permission denied.");

    const group = await Group.findOne({code: target});
    if (!group) return res.status(404).json("Group not found.");

    try {
        const messages = await Message.find({recipient: group._id});
        const finalResult = await Promise.all(messages.map(async message => {
            if (String(message.sender) !== String(currentUser._id)) {
                const sender = await User.findById(message.sender);
                return {
                    sender: {id: sender._id, email: sender.email},
                    recipient: {id: group._id, group: group.code},
                    iv: message.iv,
                    message: message.message,
                    key: message.key,
                    signature: message.signature,
                    publicKey: message.publicKey
                };
            } else {
                return {
                    sender: {id: currentUser._id, email: currentUser.email},
                    recipient: {id: group._id},
                    iv: message.iv,
                    message: message.message,
                    key: message.key,
                    signature: message.signature,
                    publicKey: message.publicKey
                };
            }
        }));
        res.json(finalResult);
    } catch {
        res.status(500).json("Something went wrong.");
    }
});

module.exports = {createMessage, messageRouter: router, startMessage, createGroupMessage};