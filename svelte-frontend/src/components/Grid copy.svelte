<!-- JS -->
<script>
    export let grid = [4, 4];
    export let board;

    $: col = `repeat(${grid[1]}, 1fr)`;
	$: row = `repeat(${grid[0]}, 1fr)`;

	function resize_grid() {
		grid = [7, 7]
	}
</script>


<!-- HTML -->
<div class="container" style="grid-template-rows: {row}; grid-template-columns: {col};">
	{#key grid}
    {#each {length: grid[0]} as _, row (row)}
        {#each {length: grid[1]} as _, col (col)}
            <div class:filled={board[row][col]}
                    on:click={() => console.log(row, col)}
                    on:mouseover={() => console.log(row, col)}
                    on:focus={() => console.log('whatever')}
                    on:contextmenu|preventDefault={console.log(row, col)}
                ></div>
        {/each}
    {/each}
	{/key}
</div>
<button on:click={resize_grid}>Change grid size</button>


<!-- CSS -->
<style>
	.container {
		display: grid;
		border: 1px solid #999;
		border-radius: 2px;
		width: 200px;
		height: 200px;
		grid-gap: 1px;
		background: #999;
		margin-bottom: 1rem;
	} 
	
	.container div {
		background: #fff;
	}	
	
	div.filled {
		background: orange;
	}
</style>