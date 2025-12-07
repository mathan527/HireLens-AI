// Dashboard JavaScript - Main functionality

// Check authentication
if (!requireAuth()) {
    throw new Error('Authentication required');
}

// Global variables
let currentResume = null;
let currentSkills = {
    all: [],
    technical: [],
    soft: [],
    tools: []
};

// Initialize dashboard
async function initDashboard() {
    // Display user email
    const userEmail = localStorage.getItem('userEmail');
    document.getElementById('userEmail').textContent = userEmail || 'User';
    
    // Load dashboard data
    await loadDashboardData();
    
    // Initialize event listeners
    initEventListeners();
}

// Load dashboard data
async function loadDashboardData() {
    try {
        showLoading(true);
        
        const data = await apiCall('/api/dashboard', {
            method: 'GET'
        });
        
        // Update stats
        document.getElementById('totalResumes').textContent = data.total_resumes || 0;
        document.getElementById('avgATSScore').textContent = data.average_ats_score || 0;
        document.getElementById('totalMatches').textContent = data.recent_matches?.length || 0;
        
        // Load latest resume if exists
        if (data.latest_resume) {
            currentResume = data.latest_resume;
            displayResumeData(currentResume);
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showLoading(false);
    }
}

// Initialize event listeners
function initEventListeners() {
    // File upload
    const resumeFile = document.getElementById('resumeFile');
    const fileUploadArea = document.getElementById('fileUploadArea');
    
    resumeFile.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = 'var(--primary-color)';
    });
    
    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.style.borderColor = 'var(--gray-light)';
    });
    
    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = 'var(--gray-light)';
        
        if (e.dataTransfer.files.length > 0) {
            resumeFile.files = e.dataTransfer.files;
            handleFileSelect({ target: resumeFile });
        }
    });
    
    // Upload form
    document.getElementById('uploadForm').addEventListener('submit', handleResumeUpload);
    
    // Job match form
    document.getElementById('jobMatchForm').addEventListener('submit', handleJobMatch);
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        if (file.type !== 'application/pdf') {
            showError('Please select a PDF file', 'uploadMessage');
            return;
        }
        document.getElementById('fileName').textContent = `Selected: ${file.name}`;
    }
}

// Handle resume upload
async function handleResumeUpload(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('resumeFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select a file', 'uploadMessage');
        return;
    }
    
    const uploadBtn = document.getElementById('uploadBtn');
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Analyzing...';
    
    // Show progress
    document.getElementById('uploadProgress').style.display = 'block';
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = getAuthToken();
        const response = await fetch(`${API_BASE_URL}/api/resume/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        const data = await response.json();
        currentResume = data;
        
        // Display results
        displayResumeData(data);
        
        // Reset form
        fileInput.value = '';
        document.getElementById('fileName').textContent = '';
        
        // Show success
        showError('✅ Resume analyzed successfully!', 'uploadMessage');
        document.getElementById('uploadMessage').classList.add('success-message');
        
        // Reload dashboard data
        await loadDashboardData();
        
    } catch (error) {
        showError(error.message, 'uploadMessage');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload & Analyze';
        document.getElementById('uploadProgress').style.display = 'none';
    }
}

// Display resume data
function displayResumeData(resume) {
    // Update ATS score
    const atsScore = Math.round(resume.ats_score);
    document.getElementById('atsScoreValue').textContent = atsScore;
    
    // Update score interpretation
    let interpretation = '';
    if (atsScore >= 80) {
        interpretation = '🎉 Excellent - Your resume is highly optimized!';
    } else if (atsScore >= 70) {
        interpretation = '👍 Good - Your resume should pass most ATS systems';
    } else if (atsScore >= 60) {
        interpretation = '⚠️ Fair - Your resume needs some improvements';
    } else {
        interpretation = '❌ Needs Work - Significant improvements required';
    }
    document.getElementById('scoreInterpretation').textContent = interpretation;
    
    // Create score chart
    createScoreChart(atsScore);
    
    // Store skills
    currentSkills = {
        all: resume.extracted_skills || [],
        technical: resume.technical_skills || [],
        soft: resume.soft_skills || [],
        tools: resume.tools || []
    };
    
    // Update skills count
    document.getElementById('skillsCount').textContent = currentSkills.all.length;
    
    // Display skills
    displaySkills('all');
    
    // Create skills chart
    createSkillsChart();
}

// Create score doughnut chart
function createScoreChart(score) {
    const canvas = document.getElementById('scoreChart');
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if any
    if (window.scoreChartInstance) {
        window.scoreChartInstance.destroy();
    }
    
    window.scoreChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [
                    score >= 80 ? '#22c55e' : score >= 60 ? '#f59e0b' : '#ef4444',
                    '#e5e7eb'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '80%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

// Display skills by category
function displaySkills(category) {
    const container = document.getElementById('skillsContainer');
    const skills = currentSkills[category];
    
    if (!skills || skills.length === 0) {
        container.innerHTML = '<p class="empty-state">No skills found in this category</p>';
        return;
    }
    
    // Use escapeHtml to prevent XSS attacks
    container.innerHTML = skills.map(skill => 
        `<span class="skill-tag">${escapeHtml(skill)}</span>`
    ).join('');
}

// Switch skills tab
function showSkillsTab(category) {
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Display skills
    displaySkills(category);
}

// Make function global
window.showSkillsTab = showSkillsTab;

// Create skills bar chart
function createSkillsChart() {
    const canvas = document.getElementById('skillsChart');
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if any
    if (window.skillsChartInstance) {
        window.skillsChartInstance.destroy();
    }
    
    window.skillsChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Technical Skills', 'Soft Skills', 'Tools'],
            datasets: [{
                label: 'Skills Count',
                data: [
                    currentSkills.technical.length,
                    currentSkills.soft.length,
                    currentSkills.tools.length
                ],
                backgroundColor: [
                    '#6366f1',
                    '#10b981',
                    '#f59e0b'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Handle job matching
async function handleJobMatch(e) {
    e.preventDefault();
    
    if (!currentResume) {
        showError('Please upload a resume first', 'uploadMessage');
        return;
    }
    
    const jobDescription = document.getElementById('jobDescription').value;
    const jobTitle = document.getElementById('jobTitle').value;
    const matchBtn = document.getElementById('matchBtn');
    
    matchBtn.disabled = true;
    matchBtn.textContent = 'Calculating...';
    
    showLoading(true);
    
    try {
        const data = await apiCall('/api/jobs/match', {
            method: 'POST',
            body: JSON.stringify({
                resume_id: currentResume.id,
                job_description: jobDescription,
                job_title: jobTitle || 'Target Position'
            })
        });
        
        // Display match results
        displayMatchResults(data);
        
        showLoading(false);
    } catch (error) {
        showError(error.message, 'uploadMessage');
        showLoading(false);
    } finally {
        matchBtn.disabled = false;
        matchBtn.textContent = 'Calculate Match';
    }
}

// Display job match results
function displayMatchResults(data) {
    const resultsDiv = document.getElementById('matchResults');
    const matchPercentage = Math.round(data.match_percentage);
    
    // Update match percentage
    document.getElementById('matchPercentage').textContent = `${matchPercentage}%`;
    
    // Update interpretation
    let interpretation = '';
    if (matchPercentage >= 80) {
        interpretation = '🎯 Excellent Match - Apply with confidence!';
    } else if (matchPercentage >= 70) {
        interpretation = '✅ Good Match - You meet most requirements';
    } else if (matchPercentage >= 60) {
        interpretation = '⚠️ Fair Match - Consider upskilling';
    } else {
        interpretation = '❌ Low Match - Significant skill gap';
    }
    document.getElementById('matchInterpretation').textContent = interpretation;
    
    // Display matched skills (with XSS protection)
    const matchedSkillsList = document.getElementById('matchedSkillsList');
    if (data.matched_skills && data.matched_skills.length > 0) {
        matchedSkillsList.innerHTML = data.matched_skills.map(skill =>
            `<span class="skill-tag" style="background: var(--success-color);">${escapeHtml(skill)}</span>`
        ).join('');
    } else {
        matchedSkillsList.innerHTML = '<p class="empty-state">No matched skills</p>';
    }
    
    // Display missing skills (with XSS protection)
    const missingSkillsList = document.getElementById('missingSkillsList');
    if (data.missing_skills && data.missing_skills.length > 0) {
        missingSkillsList.innerHTML = data.missing_skills.map(skill =>
            `<span class="skill-tag" style="background: var(--danger-color);">${escapeHtml(skill)}</span>`
        ).join('');
    } else {
        missingSkillsList.innerHTML = '<p class="empty-state">No missing skills</p>';
    }
    
    // Show results
    resultsDiv.style.display = 'block';
    
    // Display AI feedback if available (XSS protection via textContent)
    if (data.ai_feedback) {
        const feedbackCard = document.getElementById('aiFeedbackCard');
        const feedbackContent = document.getElementById('aiFeedbackContent');
        // Use textContent (not innerHTML) for XSS protection
        feedbackContent.textContent = data.ai_feedback;
        feedbackCard.style.display = 'block';
    }
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', initDashboard);
