/**
 * Elegant Calculator - JavaScript Logic
 * 
 * Built with LJPW principles:
 * - Love: Clear integration of all components
 * - Justice: Proper validation and error handling
 * - Power: Efficient calculations with keyboard support
 * - Wisdom: Well-documented with logging capability
 */

class Calculator {
    /**
     * Initialize the calculator with default state.
     */
    constructor() {
        // State
        this.currentValue = '0';
        this.previousValue = '';
        this.operation = null;
        this.shouldResetDisplay = false;
        this.history = [];
        
        // DOM Elements
        this.displayResult = document.getElementById('result');
        this.displayExpression = document.getElementById('expression');
        
        // Operator symbols for display
        this.operatorSymbols = {
            'add': '+',
            'subtract': '−',
            'multiply': '×',
            'divide': '÷'
        };
        
        // Bind methods
        this.handleButtonClick = this.handleButtonClick.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
        
        // Initialize
        this.init();
    }
    
    /**
     * Set up event listeners for buttons and keyboard.
     */
    init() {
        // Button click events
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', this.handleButtonClick);
        });
        
        // Keyboard events
        document.addEventListener('keydown', this.handleKeyPress);
        
        // Initial render
        this.updateDisplay();
        
        console.log('Calculator initialized with keyboard support');
    }
    
    /**
     * Handle button click events.
     * @param {Event} event - The click event
     */
    handleButtonClick(event) {
        const button = event.target;
        const value = button.dataset.value;
        const action = button.dataset.action;
        
        if (value !== undefined) {
            this.inputNumber(value);
        } else if (action) {
            this.executeAction(action);
        }
    }
    
    /**
     * Handle keyboard input with visual feedback.
     * @param {KeyboardEvent} event - The keyboard event
     */
    handleKeyPress(event) {
        const key = event.key;
        let buttonId = null;
        
        // Number keys
        if (/^[0-9]$/.test(key)) {
            this.inputNumber(key);
            buttonId = `btn-${key}`;
        }
        // Decimal point
        else if (key === '.' || key === ',') {
            this.executeAction('decimal');
            buttonId = 'btn-decimal';
        }
        // Operators
        else if (key === '+') {
            this.executeAction('add');
            buttonId = 'btn-add';
        }
        else if (key === '-') {
            this.executeAction('subtract');
            buttonId = 'btn-subtract';
        }
        else if (key === '*') {
            this.executeAction('multiply');
            buttonId = 'btn-multiply';
        }
        else if (key === '/') {
            event.preventDefault(); // Prevent browser search
            this.executeAction('divide');
            buttonId = 'btn-divide';
        }
        // Equals
        else if (key === 'Enter' || key === '=') {
            event.preventDefault();
            this.executeAction('equals');
            buttonId = 'btn-equals';
        }
        // Backspace
        else if (key === 'Backspace') {
            this.executeAction('delete');
            buttonId = 'btn-delete';
        }
        // Clear (Escape or 'c')
        else if (key === 'Escape' || key.toLowerCase() === 'c') {
            this.executeAction('clear');
            buttonId = 'btn-clear';
        }
        // Percent
        else if (key === '%') {
            this.executeAction('percent');
            buttonId = 'btn-percent';
        }
        
        // Visual feedback for pressed key
        if (buttonId) {
            this.animateButton(buttonId);
        }
    }
    
    /**
     * Animate a button to show keyboard press.
     * @param {string} buttonId - The ID of the button to animate
     */
    animateButton(buttonId) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.classList.add('keyboard-active');
            setTimeout(() => {
                button.classList.remove('keyboard-active');
            }, 100);
        }
    }
    
    /**
     * Input a number or digit.
     * @param {string} digit - The digit to input
     */
    inputNumber(digit) {
        if (this.shouldResetDisplay) {
            this.currentValue = '';
            this.shouldResetDisplay = false;
        }
        
        // Prevent multiple leading zeros
        if (this.currentValue === '0' && digit === '0') {
            return;
        }
        
        // Replace leading zero with digit
        if (this.currentValue === '0' && digit !== '0') {
            this.currentValue = digit;
        } else {
            // Limit display length
            if (this.currentValue.length < 15) {
                this.currentValue += digit;
            }
        }
        
        this.updateDisplay();
    }
    
    /**
     * Execute a calculator action.
     * @param {string} action - The action to execute
     */
    executeAction(action) {
        switch (action) {
            case 'clear':
                this.clear();
                break;
            case 'delete':
                this.deleteLast();
                break;
            case 'decimal':
                this.inputDecimal();
                break;
            case 'negate':
                this.negate();
                break;
            case 'percent':
                this.percent();
                break;
            case 'add':
            case 'subtract':
            case 'multiply':
            case 'divide':
                this.setOperation(action);
                break;
            case 'equals':
                this.calculate();
                break;
        }
    }
    
    /**
     * Clear all calculator state.
     */
    clear() {
        this.currentValue = '0';
        this.previousValue = '';
        this.operation = null;
        this.shouldResetDisplay = false;
        this.clearOperatorHighlight();
        this.updateDisplay();
    }
    
    /**
     * Delete the last entered digit.
     */
    deleteLast() {
        if (this.currentValue.length > 1) {
            this.currentValue = this.currentValue.slice(0, -1);
        } else {
            this.currentValue = '0';
        }
        this.updateDisplay();
    }
    
    /**
     * Input a decimal point.
     */
    inputDecimal() {
        if (this.shouldResetDisplay) {
            this.currentValue = '0';
            this.shouldResetDisplay = false;
        }
        
        if (!this.currentValue.includes('.')) {
            this.currentValue += '.';
            this.updateDisplay();
        }
    }
    
    /**
     * Negate the current value.
     */
    negate() {
        if (this.currentValue !== '0') {
            if (this.currentValue.startsWith('-')) {
                this.currentValue = this.currentValue.slice(1);
            } else {
                this.currentValue = '-' + this.currentValue;
            }
            this.updateDisplay();
        }
    }
    
    /**
     * Convert current value to percentage.
     */
    percent() {
        const value = parseFloat(this.currentValue);
        if (!isNaN(value)) {
            this.currentValue = this.formatNumber(value / 100);
            this.updateDisplay();
        }
    }
    
    /**
     * Set the current operation.
     * @param {string} op - The operation to set
     */
    setOperation(op) {
        // If there's a pending operation, calculate first
        if (this.operation && !this.shouldResetDisplay) {
            this.calculate();
        }
        
        this.previousValue = this.currentValue;
        this.operation = op;
        this.shouldResetDisplay = true;
        
        this.highlightOperator(op);
        this.updateDisplay();
    }
    
    /**
     * Perform the calculation.
     */
    calculate() {
        if (!this.operation || this.previousValue === '') {
            return;
        }
        
        const prev = parseFloat(this.previousValue);
        const curr = parseFloat(this.currentValue);
        let result;
        
        // Validate inputs
        if (isNaN(prev) || isNaN(curr)) {
            this.currentValue = 'Error';
            this.updateDisplay();
            return;
        }
        
        // Perform calculation based on operation
        switch (this.operation) {
            case 'add':
                result = prev + curr;
                break;
            case 'subtract':
                result = prev - curr;
                break;
            case 'multiply':
                result = prev * curr;
                break;
            case 'divide':
                if (curr === 0) {
                    this.currentValue = 'Error';
                    this.operation = null;
                    this.previousValue = '';
                    this.clearOperatorHighlight();
                    this.updateDisplay();
                    return;
                }
                result = prev / curr;
                break;
            default:
                return;
        }
        
        // Format and store result
        this.currentValue = this.formatNumber(result);
        
        // Log to history
        this.history.push({
            expression: `${prev} ${this.operatorSymbols[this.operation]} ${curr}`,
            result: this.currentValue
        });
        
        // Reset state
        this.operation = null;
        this.previousValue = '';
        this.shouldResetDisplay = true;
        this.clearOperatorHighlight();
        this.updateDisplay();
    }
    
    /**
     * Format a number for display.
     * @param {number} num - The number to format
     * @returns {string} The formatted number
     */
    formatNumber(num) {
        // Handle very large or very small numbers
        if (Math.abs(num) > 999999999999 || (Math.abs(num) < 0.000001 && num !== 0)) {
            return num.toExponential(6);
        }
        
        // Round to avoid floating point errors
        const rounded = Math.round(num * 1e12) / 1e12;
        
        // Convert to string and handle decimal display
        let str = rounded.toString();
        
        // Limit decimal places for display
        if (str.includes('.') && str.split('.')[1].length > 10) {
            str = rounded.toFixed(10).replace(/\.?0+$/, '');
        }
        
        return str;
    }
    
    /**
     * Highlight the active operator button.
     * @param {string} op - The operator to highlight
     */
    highlightOperator(op) {
        this.clearOperatorHighlight();
        const button = document.querySelector(`[data-action="${op}"]`);
        if (button) {
            button.classList.add('active');
        }
    }
    
    /**
     * Clear operator button highlighting.
     */
    clearOperatorHighlight() {
        document.querySelectorAll('.btn.operator').forEach(btn => {
            btn.classList.remove('active');
        });
    }
    
    /**
     * Update the calculator display.
     */
    updateDisplay() {
        // Update result
        this.displayResult.textContent = this.currentValue;
        
        // Shrink text if too long
        if (this.currentValue.length > 10) {
            this.displayResult.classList.add('shrink');
        } else {
            this.displayResult.classList.remove('shrink');
        }
        
        // Update expression
        if (this.operation && this.previousValue) {
            const symbol = this.operatorSymbols[this.operation];
            this.displayExpression.textContent = `${this.previousValue} ${symbol}`;
        } else {
            this.displayExpression.textContent = '';
        }
    }
    
    /**
     * Get calculation history.
     * @returns {Array} The calculation history
     */
    getHistory() {
        return this.history;
    }
}

// Initialize calculator when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.calculator = new Calculator();
});
