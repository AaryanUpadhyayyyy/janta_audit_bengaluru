import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const ProjectMetricsChart = ({ metrics }) => {
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Project Health Metrics Over Time',
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 1,
            },
        },
    };

    // For demo purposes, we'll create some mock historical data
    // In production, this would come from your backend
    const labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'];
    
    const data = {
        labels,
        datasets: [
            {
                label: 'True Progress',
                data: [0.2, 0.3, 0.35, 0.45, metrics.trueProgress / 100],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            },
            {
                label: 'Confidence Score',
                data: [0.4, 0.45, 0.5, 0.55, metrics.confidenceScore],
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1,
            },
            {
                label: 'Cost Performance Index',
                data: [1, 1.05, 1.08, 1.1, metrics.costPerformanceIndex],
                borderColor: 'rgb(53, 162, 235)',
                tension: 0.1,
            },
        ],
    };

    return <Line options={options} data={data} />;
};

export default ProjectMetricsChart;