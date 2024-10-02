const originalConsoleLog = console.log;
const originalConsoleError = console.error;

console.log = function (...args) {
	const consoleOutput = document.getElementById('consoleOutput');
	consoleOutput.value += args.join(' ') + '\n';
	originalConsoleLog(...args);
};

console.error = function (...args) {
	const consoleOutput = document.getElementById('consoleOutput');
	consoleOutput.value += 'Error: ' + args.join(' ') + '\n';
	originalConsoleError(...args);
};

document.getElementById('vendorIdForm').addEventListener('submit', (event) => {
	event.preventDefault();
	const vendorId = document.getElementById('vendorId').value;
	connectDevice(vendorId).then(data => {
		// Process the received data
	}).catch(error => {
		// Handle errors
	});
});

function connectDevice(vendorId) {
	const data = new Uint8Array([0x02, 0x52, 0x51, 0x48, 0x57, 0x03]);
	return navigator.usb.requestDevice({ filters: [{ vendorId: validateVendorId(vendorId) }] })
		.then(device => device.open()
		.then(() => device.selectConfiguration(1))
		.then(() => device.claimInterface(0))
		.then(() => device.transferOut(1, data))
		.then(() => device.transferIn(2))
		.then(result => {
			const data = new Uint8Array(result.data.buffer);
			console.log(Array.from(data));
			return data;
		})).catch(error => {
			console.error("Error connecting to device:", error);
			throw error;
		});
}

function validateVendorId(vendorId) {
	vendorId = vendorId.startsWith('0x') ? vendorId.slice(2) : vendorId;

	if (!/^[0-9A-F]+$/i.test(vendorId)) {
		throw new Error('Invalid vendor ID format. Must be hexadecimal (0-9, A-F).');
	}

	if (vendorId.length !== 4) {
		throw new Error('Vendor ID must be 4 characters long, e.g. 0x22B8.');
	}

	return parseInt(vendorId, 16);
}
