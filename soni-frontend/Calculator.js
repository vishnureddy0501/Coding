class Calculator {
	constructor (val) {
		this.value = val;
	}
	add (val) {
		this.value = this.value + val;
		return this;
	}
	multiply (val) {
		this.value = this.value * val;
		return this;
	}
	subtract (val) {
		this.value = this.value - val;
		return this;
	}
	getValue (val) {
	    return this.value;
	}
}
const calculator = new Calculator(2);
console.log(calculator.add(3).multiply(4).subtract(5).getValue());