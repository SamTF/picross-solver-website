<script>
	import Grid from './components/Grid.svelte'
	import Flask from './components/Flask.svelte'
	import PuzzleInfo from './components/PuzzleInfo.svelte'
	import { fade, slide, scale } from 'svelte/transition';

	
	let grid_size = 5;
	$: board = Array(grid_size).fill(0).map(_ => Array(grid_size).fill(0)) // MUST be REACTIVE so that it changes size as soon as the Grid Size also changes
	let override_blocks;
	let show_info = false;

	// Fetches a random board from the Python backend and displays it on the Grid component
	function fetch_rand_board(size) {
		fetch(`/rand_board/${size}`)
            .then(response => response.json())
            .then(response => {
				const success = response.success;
				if (success) {
					board = response.board;
					console.log(response.blocks);
					override_blocks(response.blocks);
					return board;
				}
			})
			.then(board => console.table(board))
	}

	// When the SOLVE! Button is pressed
	function on_submit(event) {
		console.log(event.detail);
		let object = JSON.stringify(event.detail) // converting the Object to a string, so it can be passed to the back-end

		// sending the JSON String to the server and fetching the response
		fetch(`/solve/${object}`)
			.then(res => res.json())
			.then(res => {
				console.log(res.success);
				if (res.success) {
					console.log('Puzzle solved successfully!');
					board = res.data;
					console.table(board);
				}
				else {
					alert('No solution possible!');
				}
			})
			// .then(board => console.table(board))	
	}

	const toggle_info = () => show_info = !show_info;
</script>

<main>
	<button class="info" on:click={toggle_info}>&#9432;</button>

	<h1>Picross Solver</h1>

	{#if show_info}
	<div transition:slide>
		<p>Hi. I'm <a href="https://sam.freelancepolice.org/" target="_blank">Sam</a> :). I made a fast Picross/Nonogram <a href="https://github.com/SamTF/pycross/" target="_blank">solving algorithm</a> in Python from scratch.</p>
		<p>This is a website UI for it built with Svelte and powered by Flask.</p>
		<p>Enter the puzzle's row and column blocks numbers seperated by a space or comma.</p>
	</div>
	{/if}

	<Grid {grid_size} {board}/>
	<button on:click={() => fetch_rand_board(grid_size)}>Random puzzle</button>
	<PuzzleInfo on:submit={on_submit} bind:grid_size={grid_size} bind:override_blocks={override_blocks}/>
</main>

<style>
	/* main {
		display: grid;
		place-items: center;
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	} */

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	/* strong {
		color: #ff3e00;
	} */

	/* @media (min-width: 640px) {
		main {
			max-width: none;
		}
	} */
</style>