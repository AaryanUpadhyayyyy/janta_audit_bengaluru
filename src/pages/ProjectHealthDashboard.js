import React, { useEffect, useState } from 'react';
import { getHealthMetrics } from '../services/healthEngineService';
import ProjectHealthMetrics from '../components/ProjectHealthMetrics';
import { Alert, Box } from '@mui/material';

const ProjectHealthDashboard = () => {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const data = await getHealthMetrics();
                setMetrics(data);
                setLoading(false);
            } catch (err) {
                setError(err);
                setLoading(false);
            }
        };

        fetchMetrics();
        
        // Refresh metrics every 5 minutes
        const interval = setInterval(fetchMetrics, 5 * 60 * 1000);
        
        return () => clearInterval(interval);
    }, []);

    if (error) {
        return (
            <Box sx={{ p: 2 }}>
                <Alert severity="error">
                    Error loading project health metrics: {error.message}
                </Alert>
            </Box>
        );
    }

    return <ProjectHealthMetrics metrics={metrics} loading={loading} error={error} />;
};

export default ProjectHealthDashboard;