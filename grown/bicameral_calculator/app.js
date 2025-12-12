/**
 * SciCalc - Scientific Calculator (Bicameral Autopoiesis)
 * ========================================================
 * 
 * LJPW Principles Embedded:
 * - Love (L: 0.900): Clear documentation, helpful feedback
 * - Justice (J: 0.700): Input validation, error messages
 * - Power (P: 0.800): Efficient calculation, error handling
 * - Wisdom (W: 0.800): Logging, history, organized code
 * 
 * Generated Harmony: 0.702
 */

// =============================================================================
// CONFIGURATION (Love: documented)
// =============================================================================

const CONFIG = {
    maxDigits: 15,
    precision: 10,
    mode: 'deg'  // 'deg' or 'rad'
};

// =============================================================================
// STATE (Wisdom: centralized)
// =============================================================================

const state = {
    expression: '',
    result: '0',
    history: [],
    mode: 'deg',
    lastAnswer: 0
};

// =============================================================================
// CALCULATOR CORE (Power: efficient)
// =============================================================================

const calculator = {
    
    /**
     * Validate input expression (Justice: prevent invalid states).
     * @param {string} expr - Expression to validate
     * @returns {boolean} Whether expression is valid
     */
    validateExpression(expr) {
        if (!expr || typeof expr !== 'string') return false;
        
        // Check for balanced parentheses
        let depth = 0;
        for (const char of expr) {
            if (char === '(') depth++;
            if (char === ')') depth--;
            if (depth < 0) return false;
        }
        
        return depth === 0;
    },

    
    /**
     * Log calculation for debugging (Wisdom: observability).
     * @param {string} context - Context of log
     * @param {string} message - Log message
     */
    log(context, message) {
        console.log(`[SciCalc:${context}] ${message}`);
    },

    /**
     * Append a number or decimal to expression.
     * @param {string} num - Number to append
     */
    appendNumber(num) {
        if (state.expression.length >= CONFIG.maxDigits * 2) return;
        state.expression += num;
        this.updateDisplay();
    },
    
    /**
     * Append an operator to expression.
     * @param {string} op - Operator (+, -, *, /)
     */
    appendOperator(op) {
        const lastChar = state.expression.slice(-1);
        if (['+', '-', '*', '/'].includes(lastChar)) {
            state.expression = state.expression.slice(0, -1);
        }
        state.expression += op;
        this.updateDisplay();
    },
    
    /**
     * Apply a scientific function.
     * @param {string} func - Function name
     */
    applyFunction(func) {
        const functions = {
            'sin': (x) => Math.sin(state.mode === 'deg' ? x * Math.PI / 180 : x),
            'cos': (x) => Math.cos(state.mode === 'deg' ? x * Math.PI / 180 : x),
            'tan': (x) => Math.tan(state.mode === 'deg' ? x * Math.PI / 180 : x),
            'log': (x) => Math.log10(x),
            'ln': (x) => Math.log(x),
            'sqrt': (x) => Math.sqrt(x),
            'pow': null,  // Handled specially
            'exp': (x) => Math.exp(x),
            'pi': () => Math.PI,
            'e': () => Math.E,
            'factorial': (x) => {
                if (x < 0 || x > 170 || !Number.isInteger(x)) return NaN;
                if (x <= 1) return 1;
                let result = 1;
                for (let i = 2; i <= x; i++) result *= i;
                return result;
            },
            'abs': (x) => Math.abs(x)
        };
        
        if (func === 'pi' || func === 'e') {
            state.expression += functions[func]().toString();
        } else if (func === 'pow') {
            state.expression += '^';
        } else {
            state.expression += func + '(';
        }
        
        this.updateDisplay();
    },
    
    /**
     * Toggle parentheses.
     */
    toggleParenthesis() {
        const openCount = (state.expression.match(/\(/g) || []).length;
        const closeCount = (state.expression.match(/\)/g) || []).length;
        
        if (openCount > closeCount) {
            state.expression += ')';
        } else {
            state.expression += '(';
        }
        this.updateDisplay();
    },
    
    /**
     * Backspace - remove last character.
     */
    backspace() {
        state.expression = state.expression.slice(0, -1);
        this.updateDisplay();
    },
    
    /**
     * Clear all.
     */
    clear() {
        state.expression = '';
        state.result = '0';
        this.updateDisplay();
    },
    
    /**
     * Negate current number.
     */
    negate() {
        if (state.expression) {
            if (state.expression.startsWith('-')) {
                state.expression = state.expression.slice(1);
            } else {
                state.expression = '-' + state.expression;
            }
        } else if (state.result !== '0') {
            state.expression = (-parseFloat(state.result)).toString();
        }
        this.updateDisplay();
    },
    
    /**
     * Calculate result (Power: robust evaluation).
     */
    calculate() {
        if (!state.expression) return;
        
        try {
            // Preprocess expression
            let expr = state.expression
                .replace(/\^/g, '**')
                .replace(/sin\(/g, 'Math.sin(' + (state.mode === 'deg' ? 'Math.PI/180*' : ''))
                .replace(/cos\(/g, 'Math.cos(' + (state.mode === 'deg' ? 'Math.PI/180*' : ''))
                .replace(/tan\(/g, 'Math.tan(' + (state.mode === 'deg' ? 'Math.PI/180*' : ''))
                .replace(/log\(/g, 'Math.log10(')
                .replace(/ln\(/g, 'Math.log(')
                .replace(/sqrt\(/g, 'Math.sqrt(')
                .replace(/exp\(/g, 'Math.exp(')
                .replace(/abs\(/g, 'Math.abs(')
                .replace(/factorial\(([^)]+)\)/g, (_, n) => {
                    const num = parseFloat(n);
                    if (num < 0 || num > 170 || !Number.isInteger(num)) return 'NaN';
                    let result = 1;
                    for (let i = 2; i <= num; i++) result *= i;
                    return result.toString();
                });
            
            // Evaluate safely (Justice: sandboxed)
            const result = Function('"use strict"; return (' + expr + ')')();
            
            if (typeof result !== 'number' || !isFinite(result)) {
                throw new Error('Invalid result');
            }
            
            // Format result
            state.result = parseFloat(result.toPrecision(CONFIG.precision)).toString();
            state.lastAnswer = parseFloat(state.result);
            
            // Add to history (Wisdom: memory)
            if (state.history.length >= 10) state.history.shift();
            state.history.push({
                expression: state.expression,
                result: state.result
            });
            
            state.expression = '';
            this.updateDisplay();
            this.updateHistory();
            
        } catch (error) {
            state.result = 'Error';
            this.updateDisplay();
            console.error('[SciCalc:Error]', error.message);
        }
    },
    
    /**
     * Update display (Love: clear feedback).
     */
    updateDisplay() {
        document.getElementById('expression').textContent = state.expression;
        document.getElementById('result').textContent = state.result;
    },
    
    /**
     * Update history panel (Wisdom: remembers).
     */
    updateHistory() {
        const panel = document.getElementById('history-panel');
        const list = document.getElementById('history-list');
        
        if (!panel || !list) return;
        
        if (state.history.length > 0) {
            panel.classList.remove('hidden');
            list.innerHTML = state.history
                .slice().reverse()
                .map(h => `<div class="history-item">${h.expression} = ${h.result}</div>`)
                .join('');
        }
    },
    
    /**
     * Set angle mode.
     * @param {string} mode - 'deg' or 'rad'
     */
    setMode(mode) {
        state.mode = mode;
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
    }
};

// =============================================================================
// EVENT LISTENERS (Love: responsive to user)
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Number buttons
    document.querySelectorAll('[data-num]').forEach(btn => {
        btn.addEventListener('click', () => calculator.appendNumber(btn.dataset.num));
    });
    
    // Operator buttons
    document.querySelectorAll('[data-op]').forEach(btn => {
        btn.addEventListener('click', () => calculator.appendOperator(btn.dataset.op));
    });
    
    // Function buttons
    document.querySelectorAll('[data-func]').forEach(btn => {
        btn.addEventListener('click', () => calculator.applyFunction(btn.dataset.func));
    });
    
    // Action buttons
    document.querySelectorAll('[data-action]').forEach(btn => {
        const actions = {
            'clear': () => calculator.clear(),
            'backspace': () => calculator.backspace(),
            'parenthesis': () => calculator.toggleParenthesis(),
            'negate': () => calculator.negate(),
            'equals': () => calculator.calculate()
        };
        btn.addEventListener('click', () => actions[btn.dataset.action]?.());
    });
    
    // Mode buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => calculator.setMode(btn.dataset.mode));
    });
    
    // Clear history
    document.getElementById('clear-history')?.addEventListener('click', () => {
        state.history = [];
        document.getElementById('history-list').innerHTML = '';
        document.getElementById('history-panel').classList.add('hidden');
    });
    
    // Keyboard support (Power: efficient input)
    document.addEventListener('keydown', (e) => {
        if (e.key >= '0' && e.key <= '9') calculator.appendNumber(e.key);
        else if (e.key === '.') calculator.appendNumber('.');
        else if (e.key === '+') calculator.appendOperator('+');
        else if (e.key === '-') calculator.appendOperator('-');
        else if (e.key === '*') calculator.appendOperator('*');
        else if (e.key === '/') { e.preventDefault(); calculator.appendOperator('/'); }
        else if (e.key === 'Enter' || e.key === '=') calculator.calculate();
        else if (e.key === 'Backspace') calculator.backspace();
        else if (e.key === 'Escape' || e.key === 'c' || e.key === 'C') calculator.clear();
        else if (e.key === '(' || e.key === ')') calculator.toggleParenthesis();
    });
    
    console.log('[SciCalc] Initialized - Grown by Bicameral Autopoiesis');
});
