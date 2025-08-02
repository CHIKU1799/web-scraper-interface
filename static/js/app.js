// Web Scraper Interface JavaScript

class WebScraperApp {
    constructor() {
        this.currentData = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkHealth();
        this.setupAutoRefresh();
    }

    bindEvents() {
        // Form submission
        document.getElementById('scrapeForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleScrape();
        });

        // Clear button
        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearResults();
        });

        // Export button
        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportData();
        });

        // URL input validation
        document.getElementById('urlInput').addEventListener('input', (e) => {
            this.validateUrl(e.target.value);
        });
    }

    validateUrl(url) {
        const urlInput = document.getElementById('urlInput');
        const scrapeBtn = document.getElementById('scrapeBtn');
        
        try {
            new URL(url);
            urlInput.classList.remove('is-invalid');
            urlInput.classList.add('is-valid');
            scrapeBtn.disabled = false;
        } catch {
            if (url.length > 0) {
                urlInput.classList.add('is-invalid');
                urlInput.classList.remove('is-valid');
            } else {
                urlInput.classList.remove('is-invalid', 'is-valid');
            }
            scrapeBtn.disabled = true;
        }
    }

    async checkHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            const modelStatus = document.getElementById('modelStatus');
            const scraperStatus = document.getElementById('scraperStatus');
            
            if (data.status === 'healthy') {
                scraperStatus.className = 'fas fa-circle text-success';
                
                if (data.models_loaded) {
                    modelStatus.className = 'fas fa-circle text-success';
                } else {
                    modelStatus.className = 'fas fa-circle text-warning';
                }
            } else {
                scraperStatus.className = 'fas fa-circle text-danger';
                modelStatus.className = 'fas fa-circle text-danger';
            }
        } catch (error) {
            console.error('Health check failed:', error);
            document.getElementById('modelStatus').className = 'fas fa-circle text-danger';
            document.getElementById('scraperStatus').className = 'fas fa-circle text-danger';
        }
    }

    setupAutoRefresh() {
        // Check health every 30 seconds
        setInterval(() => {
            this.checkHealth();
        }, 30000);
    }

    async handleScrape() {
        const url = document.getElementById('urlInput').value;
        const method = document.getElementById('methodSelect').value;
        
        if (!url) {
            this.showAlert('Please enter a valid URL', 'warning');
            return;
        }

        this.showLoading(true);
        this.hideResults();

        try {
            const response = await fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    method: method
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.currentData = data;
                this.displayResults(data);
                this.showAlert('Scraping completed successfully!', 'success');
            } else {
                throw new Error(data.error || 'Scraping failed');
            }
        } catch (error) {
            console.error('Scraping error:', error);
            this.showAlert(`Scraping failed: ${error.message}`, 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(data) {
        const { structured_data, raw_data } = data;
        
        // Display structured data
        this.displayStructuredData(structured_data);
        
        // Display raw data
        this.displayRawData(raw_data);
        
        // Display links
        this.displayLinks(raw_data.links || []);
        
        // Display images
        this.displayImages(raw_data.images || []);
        
        // Show results section
        document.getElementById('resultsSection').style.display = 'block';
        document.getElementById('welcomeMessage').style.display = 'none';
        document.getElementById('exportBtn').disabled = false;
        
        // Add fade-in animation
        document.getElementById('resultsSection').classList.add('fade-in');
    }

    displayStructuredData(data) {
        const container = document.getElementById('structuredData');
        
        if (data.error) {
            container.innerHTML = `<div class="alert alert-warning">${data.error}</div>`;
            return;
        }

        const html = `
            <div class="data-item">
                <h6><i class="fas fa-link"></i> URL</h6>
                <p>${data.url}</p>
            </div>
            <div class="data-item">
                <h6><i class="fas fa-heading"></i> Title</h6>
                <p>${data.title}</p>
            </div>
            <div class="data-item">
                <h6><i class="fas fa-file-alt"></i> AI Summary</h6>
                <p>${data.summary}</p>
            </div>
            <div class="data-item">
                <h6><i class="fas fa-chart-bar"></i> Content Statistics</h6>
                <p>Links: ${data.links_count} | Images: ${data.images_count}</p>
            </div>
            <div class="data-item">
                <h6><i class="fas fa-clock"></i> Processed At</h6>
                <p>${data.processing_timestamp}</p>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayRawData(data) {
        const container = document.getElementById('rawData');
        
        const textPreview = data.text.length > 300 
            ? data.text.substring(0, 300) + '...' 
            : data.text;
        
        const html = `
            <div class="data-item">
                <h6><i class="fas fa-file-text"></i> Text Content (Preview)</h6>
                <p style="max-height: 200px; overflow-y: auto;">${textPreview}</p>
            </div>
            <div class="data-item">
                <h6><i class="fas fa-info-circle"></i> Content Length</h6>
                <p>${data.text.length} characters</p>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayLinks(links) {
        const container = document.getElementById('extractedLinks');
        
        if (links.length === 0) {
            container.innerHTML = '<p class="text-muted">No links found</p>';
            return;
        }

        const linksHtml = links.slice(0, 10).map(link => 
            `<a href="${link}" target="_blank" class="link-item">
                <i class="fas fa-external-link-alt"></i> ${link}
            </a>`
        ).join('');
        
        container.innerHTML = linksHtml;
    }

    displayImages(images) {
        const container = document.getElementById('extractedImages');
        
        if (images.length === 0) {
            container.innerHTML = '<p class="text-muted">No images found</p>';
            return;
        }

        const imagesHtml = images.slice(0, 5).map(image => 
            `<a href="${image}" target="_blank" class="image-item">
                <i class="fas fa-image"></i> ${image}
            </a>`
        ).join('');
        
        container.innerHTML = imagesHtml;
    }

    clearResults() {
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('welcomeMessage').style.display = 'block';
        document.getElementById('exportBtn').disabled = true;
        document.getElementById('urlInput').value = '';
        document.getElementById('urlInput').classList.remove('is-valid', 'is-invalid');
        document.getElementById('scrapeBtn').disabled = true;
        this.currentData = null;
    }

    exportData() {
        if (!this.currentData) {
            this.showAlert('No data to export', 'warning');
            return;
        }

        const dataStr = JSON.stringify(this.currentData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `scraped_data_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        this.showAlert('Data exported successfully!', 'success');
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        const scrapeBtn = document.getElementById('scrapeBtn');
        
        if (show) {
            spinner.style.display = 'block';
            scrapeBtn.disabled = true;
            scrapeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scraping...';
        } else {
            spinner.style.display = 'none';
            scrapeBtn.disabled = false;
            scrapeBtn.innerHTML = '<i class="fas fa-search"></i> Scrape & Analyze';
        }
    }

    hideResults() {
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('welcomeMessage').style.display = 'none';
    }

    showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert alert at the top of main content
        const mainContent = document.querySelector('.main-content');
        mainContent.insertBefore(alertDiv, mainContent.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WebScraperApp();
}); 