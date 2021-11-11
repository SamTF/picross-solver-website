<!-- # This is a temp component that gathers all the info input required to solve a nonogram puzzle  -->

<!-- JS -->
<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();


    export let grid_size = 5;                                       // the size of the picross puzzle grid, set from the number input
    $: range = [...Array(grid_size).keys()]                         // creates a range array : range(grid_size)
    $: Blocks = {                                                   // object to hold all the blocks, with arrays of length grid size to store each axies/line's block value
        rows: Array(grid_size).fill("0"),
        cols: Array(grid_size).fill("0")
    }
    let prevBlocks = {rows: [], cols: []}

    // Dispatching the input data object on submit
    function on_submit() {
        // Checking if there are empty values
        if (check_for_empty()) {
            console.log('>>>ERROR: Empty Input!\nAll input boxes must be filled with numbers. Write \'0\' if line is empty.');
            return;
        }

        // Checking if every input is valid (only integers)
        let valid = false;
        try {
            valid = validate_all_input();
        } catch (TypeError) {
            console.log("Puzzle has already been solved!");
            alert("Puzzle has already been solved!");
            return;
        }
        
        if (!valid) {
            console.log('>>> ERROR: Invalid Input!\nInput must ONLY contain numbers.');
            alert("Invalid Input! Input must ONLY contain numbers.");
            return;
        }

        // Checks for block overflow
        if (Object.values(Blocks).some(element => element.some(overflow))) {
            console.error('>>> ERROR: Some Blocks OVERFLOW and require more spaces than are available. Double check your data.');
            alert("Some blocks require more spaces than the grid size. Double check your numbers!");
            return;
        }

        
        const formattedBlocks = format_input(Blocks);                           // Formating the Blocks CLIENT-SIDE from 1D Array of strings to 2D Array of Ints
        if (JSON.stringify(formattedBlocks) == JSON.stringify(prevBlocks)) {    // Checking if this puzzle has already been submitted and solved
            console.log("You already solved this puzzle!");
            alert("Puzzle has already been solved!");
            return;
        }
        prevBlocks = formattedBlocks;                                           // Saving this value so we don't repeat Solves and flood the server

        // Dispatching the event + data
        dispatch('submit', formattedBlocks);
        console.log('>>> INPUT SUBMITTED SUCCESSFULLY!');
        console.log(Blocks)
    }

    // Checks if there any input elements with empty values
    function check_for_empty() {
        return Object.values(Blocks).some(element => element.includes(undefined)) // True if SOME(any in Python) axis array in the Object values INCLUDES an undefined value
    }

    // Runs the check_input function for every element in every key's array // object.values returns an array on sub-arrays, then we check every element in the sub-array, for every element in the main array
    function validate_all_input() {
        return (Object.values(Blocks).every(element => element.every(check_input))); 
    }

    // Checking if every character in the input block is a number
    function check_input(input_string) {
        // const blocks = input_string.split(" ");             // splitting the string into an array seperated by spaces
        const blocks = input_string.split(/[ ,]+/);         // !! splitting by whitespace OR comma !! -> https://stackoverflow.com/questions/10346722/how-to-split-a-string-by-white-space-or-comma
        return blocks.every( element => isInt(element));    // checking if every element in the array is an int
    }

    // Using REGEX to check if a string ONLY contains numbers (not letters or special characters like dots)
    const isInt = (value) => /^\d+$/.test(value); //https://stackoverflow.com/questions/37674069/javascript-check-if-string-can-be-converted-to-integer/37674281


    // Formats the user input from an array of strings, to a nested array of ints, for use in the backend
    function format_input(Blocks) {
        let fBlocks = { rows: [], cols: []} // creating a new Object to store formatted values so as to not override the original
        // splits input by whitespace and comma; removes empty strings; converts str to int)
        for (const key in Blocks) {
            fBlocks[key] = Blocks[key].map( element => element.split(/[ ,]+/).filter(e => e).map(Number) );
        }
        return fBlocks;
    }

    // Checks if the blocks in this line overflow beyond the cell size limit
    function overflow(input_string) {
        let blocks = input_string.split(" ").map(Number);   // splitting the string into an array seperated by spaces, and converting all strings to numbers
        let sum = blocks.reduce((sum, num) => sum + num);   // summing all numbers in the array
        let min_spaces = sum + (blocks.length - 1);         // min spaces needed = sum of all blocks + gap of at least 1 space between each block

        return min_spaces > grid_size;                      // True if the block overflows and requires more spaces than are available
    }

    // Changes the data in the Input blocks to match the random puzzle just generated
    export function override_blocks(new_blocks) {
        console.log("HELLLLOOOO!!!");
        if (!new_blocks.hasOwnProperty('rows')) {
                console.error('Object does not have the required properties');
                return;
        } if (new_blocks.rows.length == grid_size) {
            Blocks = new_blocks;
        } else {
            console.error("Grid sizes don't match!");
        }
    }

    format_input();
</script>


<!-- HTML -->
<form>
    <div class="grid-size">
        <!-- <strong>Grid Size: </strong> -->
        <input type="number" min="5" max="15" placeholder="Grid size" bind:value={grid_size}>
    </div>
    
    <div class="rows">
        <strong><p>Row blocks:</p></strong>
        <div class="input-blocks">   
        {#each range as r}
            <input type="text" placeholder="{r+1}" bind:value={Blocks.rows[r]} title="Enter block numbers seperated by space or comma">
        {/each}
        </div>
    </div>

    <div class="columns">
        <strong><p>Column blocks:</p></strong>
        <div class="input-blocks"> 
        {#each range as r}
            <input type="text" placeholder="{r+1}" bind:value={Blocks.cols[r]} title="Enter block numbers seperated by space or comma">
        {/each}
        </div>
    </div>

    <button class="btn-large" on:click|preventDefault={on_submit}>SOLVE!</button>
</form>


<!-- CSS -->
<!-- <style>
    input {
        max-width: 5vw;
    }
</style> -->