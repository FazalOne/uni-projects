const express = require('express');
const router = express.Router();
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json();
const User = require('../models/user.model');

require('dotenv').config();
const SECURITY_KEY = process.env.SECURITY_KEY;

const generateToken = () => {
    const randomToken = require('random-token').create(SECURITY_KEY);
    return randomToken(50);
}

// Get all users (emails only)
router.post('/get_all_users', jsonParser, (req, res) => {
    if (!req.body.key) return res.status(403).json("Permission denied.");
    if (req.body.key !== SECURITY_KEY) return res.status(403).json("Permission denied.");

    User.find({})
        .then(users => {
            const emails = users.map(user => user.email);
            res.json(emails);
        })
        .catch(err => res.status(500).json("Error: " + err));
});

// Get user by token and renew token
router.post('/get_by_token/', jsonParser, (req, res) => {
    if (req.body.SECURITY_KEY !== SECURITY_KEY) return res.status(403).json("Permission denied.");

    User.findOne({ token: req.body.token }, (err, user) => {
        if (err) return res.status(500).json("Error: " + err);
        if (!user) return res.status(404).json("User not found.");

        user.token = generateToken();
        user.save()
            .then(() => res.json(user))
            .catch(err => res.status(500).json("Error: " + err));
    });
});

// Get user by ID
router.post('/get_by_id/', jsonParser, (req, res) => {
    if (!req.body.key) return res.status(403).json("Permission denied.");
    if (req.body.key !== SECURITY_KEY) return res.status(403).json("Permission denied.");

    User.findById(req.body.id)
        .then(user => res.json(user))
        .catch(err => res.status(500).json("Error: " + err));
});

// Register new user
router.post('/register', jsonParser, (req, res) => {
    const { name, password, email } = req.body;

    User.findOne({ email }, (err, user) => {
        if (err) return res.status(500).json("Error has occurred. Please refresh page");
        if (user) return res.status(400).json("Email has been taken.");

        const token = generateToken();
        const newUser = new User({ name, password, email, token });

        newUser.save()
            .then(() => res.json({ "Message": "Success", token }))
            .catch(err => res.status(500).json(err));
    });
});

// Login user
router.post('/login', jsonParser, (req, res) => {
    const { email, password } = req.body;

    User.findOne({ email }, (err, user) => {
        if (err) return res.status(500).json("Error has occurred.");
        if (!user) return res.status(400).json("User not found");

        user.comparePassword(password, (err, isMatch) => {
            if (err) return res.status(500).json("Error occurred.");
            if (isMatch) {
                const token = generateToken();
                user.token = token;
                user.save();
                return res.json({ "message": "Success", token });
            } else {
                return res.status(400).json("Password doesn't match");
            }
        });
    });
});

// Update user (email/name)
router.post('/update', jsonParser, (req, res) => {
    const token = req.body.token;
    if (!token) return res.status(403).json("Permission denied.");

    User.findOne({ token: token, email: req.body.email }, (err, user) => {
        if (err) return res.status(500).json("Something went wrong.");
        if (!user) return res.status(404).json("User not found.");

        user.token = generateToken();
        user.email = req.body.new_email;
        user.name = req.body.name;

        user.save()
            .then(() => res.json({ message: "Updated", user }))
            .catch(err => res.status(500).json(err));
    });
});

module.exports = router;
