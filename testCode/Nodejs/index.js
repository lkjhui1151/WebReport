let example1 = [5, 7, 6];

example1.push(8, 9, 10);
//The more number u add to the push code, more number will add on the sequence
example1.pop();
//Will remove the last number in the sequence


example1[0] = 1;
//Overwrite values Target values and reset the value on that index 0

example1.forEach((element) => {
    console.log(element)
});

//The entire array use a forEach statement
console.log(example1)