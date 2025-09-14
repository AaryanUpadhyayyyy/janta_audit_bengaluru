const express = require('express');
const router = express.Router();
const { getHealthMetrics } = require('../controllers/healthEngineController');

router.get('/health-metrics', getHealthMetrics);

module.exports = router;