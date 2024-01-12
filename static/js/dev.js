document.addEventListener('DOMContentLoaded', function () {
    var skipEncodingCheckbox = document.getElementById('skipEncodingCheckbox');
    var encoderGroupContainer = document.getElementById('encoderGroup');
    var encodeOtherColumnBtn = document.getElementById('encodeOtherColumnBtn');
    var removeEncodedColumnBtn = document.getElementById('removeEncodedColumnBtn');

    skipEncodingCheckbox.addEventListener('change', function () {
        toggleEncoderComponents(!this.checked);
        toggleAddDeleteButtons(!this.checked);
    });

    encodeOtherColumnBtn.addEventListener('click', function () {
        if (!skipEncodingCheckbox.checked) {
            addNewEncoderGroup();
            updateCatColsSelect();
            toggleAddDeleteButtons(true);
        }
    });

    removeEncodedColumnBtn.addEventListener('click', function () {
        if (!skipEncodingCheckbox.checked) {
            removeLastEncoderGroup();
            updateCatColsSelect();
            toggleAddDeleteButtons(true);
        }
    });

    function addNewEncoderGroup() {
        var newEncoderGroup = encoderGroupContainer.cloneNode(true);
        newEncoderGroup.style.display = 'flex';
        encoderGroupContainer.parentNode.appendChild(newEncoderGroup);
    }

    function removeLastEncoderGroup() {
        var encoderGroups = document.querySelectorAll('.encoder-group');
        if (encoderGroups.length > 1) {
            var lastEncoderGroup = encoderGroups[encoderGroups.length - 1];
            lastEncoderGroup.parentNode.removeChild(lastEncoderGroup);
        }
    }

    function toggleEncoderComponents(enable) {
        encoderGroupContainer.querySelectorAll('select').forEach(function (element) {
            element.disabled = !enable;
        });
    }

    function toggleAddDeleteButtons(enable) {
        encodeOtherColumnBtn.disabled = !enable || encoderGroupContainer.children.length >= document.querySelectorAll('#categoricalColumnsSelect option:enabled').length;
        removeEncodedColumnBtn.disabled = !enable || encoderGroupContainer.children.length <= 1;
    }

    function updateCatColsSelect() {
        var selectedCols = [];
        document.querySelectorAll('.encoder-group select[name="cat_cols"]').forEach(function (select) {
            selectedCols.push(select.value);
        });

        document.querySelectorAll('#categoricalColumnsSelect option').forEach(function (option) {
            option.disabled = selectedCols.includes(option.value);
        });
    }

    // Initial state based on the "Skip encoding" checkbox
    toggleEncoderComponents(!skipEncodingCheckbox.checked);
    toggleAddDeleteButtons(!skipEncodingCheckbox.checked);

    updateCatColsSelect();
});
