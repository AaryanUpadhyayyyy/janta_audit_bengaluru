import React from 'react';
import { CircularProgress, Typography, Box, Paper, Grid } from '@mui/material';
import ProjectMetricsChart from './ProjectMetricsChart';
import { green, orange, red } from '@mui/material/colors';

const StatusIndicator = ({ status }) => {
    const getStatusColor = () => {
        switch (status) {
            case 'GREEN':
                return green[500];
            case 'YELLOW':
                return orange[500];
            case 'RED':
                return red[500];
            default:
                return 'gray';
        }
    };

    return (
        <Box
            sx={{
                width: 16,
                height: 16,
                borderRadius: '50%',
                backgroundColor: getStatusColor(),
                display: 'inline-block',
                marginRight: 1
            }}
        />
    );
};

const MetricCard = ({ title, value, unit }) => (
    <Paper
        elevation={2}
        sx={{
            p: 2,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center'
        }}
    >
        <Typography variant="subtitle2" color="text.secondary">
            {title}
        </Typography>
        <Typography variant="h5" component="div">
            {value}
            {unit && <Typography component="span" variant="caption" sx={{ ml: 0.5 }}>{unit}</Typography>}
        </Typography>
    </Paper>
);

const ProjectHealthMetrics = ({ metrics, loading, error }) => {
    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ p: 2 }}>
                <Typography color="error">Error loading metrics: {error.message}</Typography>
            </Box>
        );
    }

    if (!metrics) {
        return null;
    }

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Project Health Dashboard
            </Typography>
            
            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 3, mb: 3 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <StatusIndicator status={metrics.status} />
                            <Typography variant="h6">
                                Project Status: {metrics.status}
                            </Typography>
                        </Box>
                        <Typography variant="body1" paragraph>
                            Predicted Completion: {metrics.predictedCompletion}
                        </Typography>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Grid container spacing={2}>
                        <Grid item xs={6}>
                            <MetricCard
                                title="True Progress"
                                value={`${metrics.trueProgress}%`}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <MetricCard
                                title="Confidence Score"
                                value={metrics.confidenceScore.toFixed(2)}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <MetricCard
                                title="Cost Performance"
                                value={metrics.costPerformanceIndex.toFixed(2)}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <MetricCard
                                title="Data Points"
                                value={metrics.systemHealth.dataPoints}
                            />
                        </Grid>
                    </Grid>
                </Grid>

                <Grid item xs={12}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            System Health Indicators
                        </Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={4}>
                                <MetricCard
                                    title="Average Variance"
                                    value={metrics.systemHealth.avgVariance.toFixed(3)}
                                />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <MetricCard
                                    title="Model Confidence"
                                    value={metrics.systemHealth.modelConfidence.toFixed(2)}
                                />
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>

                <Grid item xs={12}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Metrics Trend
                        </Typography>
                        <Box sx={{ height: 400 }}>
                            <ProjectMetricsChart metrics={metrics} />
                        </Box>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default ProjectHealthMetrics;