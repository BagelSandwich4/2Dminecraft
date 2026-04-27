"""
Contains all the collision logic
"""

def solid_mask(instance, player):
    """
    Turns collisions on for any entity so you cant pass through the sprite
    Inputs:
        instance - class instance of the entity
        player - instance of the Player class in 2d_minecraft
    """
    if player.vel.y > 0:
        # 1. Calculate offset to check if we are touching the platform at all
        offset_x = int(instance.pos[0] - player.pos.x)
        offset_y = int(instance.pos[1] - player.pos.y)

        if player.mask.overlap(instance.mask, (offset_x, offset_y)):

            # 2. Find the EXACT pixel coordinate on the platform we hit
            instance_offset_x = int(player.pos.x - instance.pos[0])
            instance_offset_y = int(player.pos.y - instance.pos[1])
            instance_hit = instance.mask.overlap(
                player.mask, (instance_offset_x, instance_offset_y)
            )

            if instance_hit:
                # plat_hit[1] is the local Y coordinate on the platform.
                # Add plat.pos[1] to get the absolute
                # world Y coordinate of the floor.
                floor_y = instance.pos[1] + instance_hit[1]
                # 3. Only snap if the floor is below
                # the upper section of the player.
                # This prevents the player
                # from instantly climbing a vertical wall
                # when walking into it, but allows them
                # to walk on lower floors inside a large image!
                if floor_y > player.pos.y + (player.image.get_height() * 0.25):
                    player.pos.y = floor_y - player.image.get_height()
                    player.vel.y = 0
                    player.grounded = True
