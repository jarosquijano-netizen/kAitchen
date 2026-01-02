/**
 * Frontend tests using a simple test framework
 * Run with: node tests/test_frontend.js
 */

// Simple test framework
class TestFramework {
    constructor() {
        this.tests = [];
        this.passed = 0;
        this.failed = 0;
    }

    test(name, fn) {
        this.tests.push({ name, fn });
    }

    async run() {
        console.log('Running frontend tests...\n');
        
        for (const test of this.tests) {
            try {
                await test.fn();
                console.log(`✓ ${test.name}`);
                this.passed++;
            } catch (error) {
                console.error(`✗ ${test.name}`);
                console.error(`  Error: ${error.message}`);
                this.failed++;
            }
        }

        console.log(`\nResults: ${this.passed} passed, ${this.failed} failed`);
        return this.failed === 0;
    }

    assert(condition, message) {
        if (!condition) {
            throw new Error(message || 'Assertion failed');
        }
    }

    assertEqual(actual, expected, message) {
        if (actual !== expected) {
            throw new Error(message || `Expected ${expected}, got ${actual}`);
        }
    }

    assertTrue(condition, message) {
        this.assert(condition, message || 'Expected true');
    }

    assertFalse(condition, message) {
        this.assert(!condition, message || 'Expected false');
    }
}

// Mock API for testing
class MockAPI {
    constructor() {
        this.reset();
    }
    
    reset() {
        this.data = {
            adults: [],
            children: [],
            recipes: []
        };
    }

    async get(endpoint) {
        if (endpoint === '/api/adults') {
            return {
                success: true,
                data: this.data.adults,
                count: this.data.adults.length
            };
        }
        if (endpoint === '/api/children') {
            return {
                success: true,
                data: this.data.children,
                count: this.data.children.length
            };
        }
        if (endpoint === '/api/family/summary') {
            return {
                success: true,
                data: {
                    adults: this.data.adults,
                    children: this.data.children,
                    total_members: this.data.adults.length + this.data.children.length
                }
            };
        }
        throw new Error(`Unknown endpoint: ${endpoint}`);
    }

    async post(endpoint, data) {
        if (endpoint === '/api/adults') {
            const adult = { ...data, id: this.data.adults.length + 1 };
            this.data.adults.push(adult);
            return { success: true, id: adult.id };
        }
        if (endpoint === '/api/children') {
            const child = { ...data, id: this.data.children.length + 1 };
            this.data.children.push(child);
            return { success: true, id: child.id };
        }
        throw new Error(`Unknown endpoint: ${endpoint}`);
    }

    async delete(endpoint) {
        const match = endpoint.match(/\/api\/(adults|children)\/(\d+)/);
        if (match) {
            const type = match[1];
            const id = parseInt(match[2]);
            const array = this.data[type];
            const index = array.findIndex(item => item.id === id);
            if (index !== -1) {
                array.splice(index, 1);
                return { success: true };
            }
        }
        throw new Error(`Unknown endpoint: ${endpoint}`);
    }
}

// Test suite
const test = new TestFramework();
const api = new MockAPI();

// Test API methods
test.test('API GET /api/adults returns empty list', async () => {
    const result = await api.get('/api/adults');
    test.assertTrue(result.success);
    test.assertEqual(result.count, 0);
    test.assertEqual(result.data.length, 0);
});

test.test('API POST /api/adults adds adult', async () => {
    const adult = {
        nombre: 'Test Adult',
        edad: 30,
        objetivo_alimentario: 'Test'
    };
    const result = await api.post('/api/adults', adult);
    test.assertTrue(result.success);
    test.assertTrue(result.id > 0);
    
    const getResult = await api.get('/api/adults');
    test.assertEqual(getResult.count, 1);
    test.assertEqual(getResult.data[0].nombre, 'Test Adult');
});

test.test('API DELETE /api/adults removes adult', async () => {
    // Reset API state
    api.reset();
    
    // Add adult first
    const addResult = await api.post('/api/adults', {
        nombre: 'To Delete',
        edad: 25
    });
    
    // Verify it was added
    let getResult = await api.get('/api/adults');
    test.assertEqual(getResult.count, 1);
    
    // Delete it
    const deleteResult = await api.delete(`/api/adults/${addResult.id}`);
    test.assertTrue(deleteResult.success);
    
    // Verify deleted
    getResult = await api.get('/api/adults');
    test.assertEqual(getResult.count, 0);
});

test.test('API GET /api/family/summary returns correct count', async () => {
    // Reset API state
    api.reset();
    
    // Add some profiles
    await api.post('/api/adults', { nombre: 'Adult 1', edad: 30 });
    await api.post('/api/children', { nombre: 'Child 1', edad: 8 });
    
    const result = await api.get('/api/family/summary');
    test.assertTrue(result.success);
    test.assertEqual(result.data.total_members, 2);
    test.assertEqual(result.data.adults.length, 1);
    test.assertEqual(result.data.children.length, 1);
});

// Test utility functions
test.test('Test assertEqual works correctly', () => {
    test.assertEqual(1, 1);
    test.assertEqual('test', 'test');
});

test.test('Test assertTrue works correctly', () => {
    test.assertTrue(true);
    test.assertTrue(1 === 1);
});

test.test('Test assertFalse works correctly', () => {
    test.assertFalse(false);
    test.assertFalse(1 === 2);
});

// Run tests
if (typeof module !== 'undefined' && module.exports) {
    // Node.js environment
    module.exports = { test, MockAPI };
    test.run().then(success => {
        process.exit(success ? 0 : 1);
    });
} else {
    // Browser environment
    test.run();
}
