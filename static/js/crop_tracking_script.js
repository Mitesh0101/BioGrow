document.addEventListener('DOMContentLoaded', function() {
    
    const farmSelect = document.getElementById('farmSelect');
    const formContainer = document.getElementById('trackingFormContainer');
    const farmNameDisplay = document.getElementById('selectedFarmName');
    const cropInfoDisplay = document.getElementById('selectedCropInfo');
    const activeFarmInput = document.getElementById('activeFarmId');
    const weekBadge = document.getElementById('currentWeekBadge');
    const establishmentCard = document.getElementById('cardEstablishment');
    const submitBtn = document.getElementById('submitLogBtn');
    const alertArea = document.getElementById('alertArea');

    // 1. Handle Farm Selection
    farmSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        
        if (selectedOption.value) {
            // Get data attributes
            const farmId = selectedOption.value;
            const farmLabel = selectedOption.text.split('(')[0]; // Extract name
            const cropName = selectedOption.getAttribute('data-crop-name');
            const weekNum = parseInt(selectedOption.getAttribute('data-week'));

            // Populate UI
            farmNameDisplay.textContent = farmLabel;
            cropInfoDisplay.textContent = cropName;
            activeFarmInput.value = farmId;
            weekBadge.textContent = `Week ${weekNum}`;

            // Logic: Hide Establishment Card if Week > 4
            if (weekNum > 4) {
                establishmentCard.classList.add('d-none');
            } else {
                establishmentCard.classList.remove('d-none');
            }
            
            formContainer.classList.remove('d-none');
        }
    });

    // 2. Handle Form Submission
    submitBtn.addEventListener('click', function() {
        const farmId = activeFarmInput.value;
        const formData = new FormData(document.getElementById('fieldLogForm'));

        // Reset Alerts
        alertArea.innerHTML = '';
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';

        fetch(`/log_field_data/${farmId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i data-lucide="save" class="me-2"></i> Save Field Log';
            lucide.createIcons(); // Re-init icons

            // Show Alerts (The Roast/Advice)
            if (data.alerts && data.alerts.length > 0) {
                let alertHTML = '';
                data.alerts.forEach(alert => {
                    alertHTML += `
                        <div class="alert alert-warning alert-custom alert-dismissible fade show shadow-sm" role="alert">
                            <div class="d-flex align-items-center">
                                <i data-lucide="alert-triangle" class="me-2"></i>
                                <div>${alert}</div>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `;
                });
                alertArea.innerHTML = alertHTML;
                lucide.createIcons();
            } else {
                // Success Message
                alertArea.innerHTML = `
                    <div class="alert alert-success alert-dismissible fade show shadow-sm" role="alert">
                        <i data-lucide="check-circle" class="me-2"></i>
                        <strong>Log Saved!</strong> Great job keeping your records updated.
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                `;
                lucide.createIcons();
                // Optional: Reset form or scroll to top
                // document.getElementById('fieldLogForm').reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Save Field Log';
            alert('An error occurred. Please try again.');
        });
    });
});