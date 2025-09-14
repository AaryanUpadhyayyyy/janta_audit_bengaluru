const { spawn } = require('child_process');
const path = require('path');

const getHealthMetrics = async (req, res) => {
    try {
        const pythonScript = path.join(__dirname, '../../python_scripts/hybrid_health_engine/run.py');
        
        // Detect platform and use appropriate Python executable
        let pythonExecutable = 'python3';
        if (process.platform === 'win32') {
            pythonExecutable = 'python';
        }
        
        // Try to use virtual environment if available
        const venvPython = path.join(__dirname, '../../.venv/bin/python');
        if (require('fs').existsSync(venvPython)) {
            pythonExecutable = venvPython;
        }
        
        const pythonProcess = spawn(pythonExecutable, [pythonScript]);

        let dataString = '';
        let errorString = '';

        pythonProcess.stdout.on('data', (data) => {
            dataString += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorString += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({ 
                    error: 'Error running health engine',
                    details: errorString
                });
            }

            // Parse the output to extract metrics
            const metrics = parseHealthMetrics(dataString);
            res.json(metrics);
        });
    } catch (error) {
        res.status(500).json({ 
            error: 'Server error', 
            details: error.message 
        });
    }
};

function parseHealthMetrics(output) {
    try {
        const lines = output.split('\n');
        const metrics = {
            trueProgress: null,
            predictedCompletion: null,
            status: null,
            confidenceScore: null,
            costPerformanceIndex: null,
            systemHealth: {
                dataPoints: null,
                avgVariance: null,
                modelConfidence: null
            }
        };

        let currentSection = null;
        for (const line of lines) {
            if (line.includes('Project Health Metrics:')) {
                currentSection = 'metrics';
                continue;
            } else if (line.includes('System Health:')) {
                currentSection = 'system';
                continue;
            }

            const trimmedLine = line.trim();
            if (currentSection === 'metrics') {
                if (trimmedLine.startsWith('True Progress:')) {
                    metrics.trueProgress = parseFloat(trimmedLine.split(':')[1].trim().replace('%', ''));
                } else if (trimmedLine.startsWith('Predicted Completion:')) {
                    metrics.predictedCompletion = trimmedLine.split(':')[1].trim();
                } else if (trimmedLine.startsWith('Status:')) {
                    metrics.status = trimmedLine.split(':')[1].trim().replace('ProgressStatus.', '');
                } else if (trimmedLine.startsWith('Confidence Score:')) {
                    metrics.confidenceScore = parseFloat(trimmedLine.split(':')[1].trim());
                } else if (trimmedLine.startsWith('Cost Performance Index:')) {
                    metrics.costPerformanceIndex = parseFloat(trimmedLine.split(':')[1].trim());
                }
            } else if (currentSection === 'system') {
                if (trimmedLine.startsWith('data_points:')) {
                    metrics.systemHealth.dataPoints = parseInt(trimmedLine.split(':')[1].trim());
                } else if (trimmedLine.startsWith('avg_variance:')) {
                    metrics.systemHealth.avgVariance = parseFloat(trimmedLine.split(':')[1].trim());
                } else if (trimmedLine.startsWith('model_confidence:')) {
                    metrics.systemHealth.modelConfidence = parseFloat(trimmedLine.split(':')[1].trim());
                }
            }
        }

        return metrics;
    } catch (error) {
        throw new Error(`Error parsing metrics: ${error.message}`);
    }
}

module.exports = {
    getHealthMetrics
};