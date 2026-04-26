def blocks_to_pixels(blocks):
    '''
    Converts our in-game unit of "blocks" into pixels.
    Input:
        blocks - integer representing number of blocks to be converted
    Output:
        blocks times 16
    '''
    return blocks * 16