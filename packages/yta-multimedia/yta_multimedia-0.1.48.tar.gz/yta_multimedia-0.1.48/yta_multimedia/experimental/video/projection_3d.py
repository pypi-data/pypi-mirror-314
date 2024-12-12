"""
This file has been created to preserve a part of code
that was able to project images to simulate a 3D 
effect and also being able to put those images in
front of other videos with a mask.

TODO: This is experimental, as you can see, but the
results are very nice to make some preset or similar
"""

def test_perspective(angle: float, output_filename: str):
    # Use one image to calculate the projection
    import cv2
    import numpy as np

    image_to_inject = cv2.imread('C:/Users/dania/Desktop/004_youtube_video.png')
    image = cv2.imread('C:/Users/dania/Desktop/white_1920x1080.png')

    # Adapt the original image
    original_image_height, original_image_width = image_to_inject.shape[:2]
    shape_to_inject = np.array([
        [0, 0],
        [original_image_width - 1, 0],
        [original_image_width - 1, original_image_height - 1],
        [0, original_image_height - 1]
    ], dtype = 'float32')
    
    # We need to apply a resize first to make sure it fits our
    # expected dimensions, then we will adjust it and apply the
    # rotation that will change the actual dimensions as the
    # width and height changes according to the rotation, so we
    # would need to move the element again

    # First I will use static corners just to reduce its size
    # TODO: This can be dynamic according to what we need, or
    # it should be the maximum possible to fit the 1920x1080
    # dimensions without being out of it. By now it is a 3rd
    # of the region size
    desired_width = 1920 / 3
    desired_height = 1080 / 3
    x_start = 1920 / 2 - (desired_width / 2)
    y_start = 1080 / 2 - (desired_height / 2)

    # Build corners to make it possible
    corners = np.array([
        (x_start, y_start),
        (x_start + desired_width, y_start),
        (x_start + desired_width, y_start + desired_height),
        (x_start, y_start + desired_height)
    ], dtype = 'float32')

    # We need the angle in radians
    angle = np.radians(angle)
    # Rz = np.array([
    #     [np.cos(angle), -np.sin(angle), 0],
    #     [np.sin(angle), np.cos(angle), 0],
    #     [0, 0, 1]
    # ], dtype = 'float32')
    def x_rotation(angle: float):
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ], dtype = 'float32')
    
    def y_rotation(angle: float):
        return np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ], dtype = 'float32')
    
    def z_rotation(angle: float):
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ], dtype = 'float32')
    # Here we are applying the rotation we want, just play
    # with this. This will change again the image shape
    # so we need to adjust the position later
    # TODO: Play with this please
    Rz = z_rotation(angle)
    # Rz = np.array([
    #     [np.cos(angle), 0, -np.sin(angle)],
    #     [np.sin(angle), np.cos(angle), 0],
    #     [0, 0, 1]
    # ], dtype = 'float32')

    # 2D to 3D adding a 0 z coordinate
    pts3d = np.hstack((corners, np.zeros((corners.shape[0], 1))))

    # Apply rotation, so these are our new coordinates
    # with the rotation applied. We should need to make
    # a fix to put it in the middle of the scene 
    # according to the new size
    pts3d_rotadas = np.dot(pts3d, Rz.T)

    # Now we need to fix the position by size
    x_coords = [coord[0] for coord in pts3d_rotadas]
    y_coords = [coord[1] for coord in pts3d_rotadas]

    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)
    max_width_after_rotation = x_max - x_min
    max_height_after_rotation = y_max - y_min

    # This is the new x position to let it be in the
    # center
    new_start_x = 1920 / 2 - max_width_after_rotation / 2
    new_start_y = 1080 / 2 - max_height_after_rotation / 2
    dif_x = x_min - new_start_x
    dif_y = y_min - new_start_y

    # Add the needed amount of movement to let it be in the
    # center of the scene but keeping the rotation
    for pts3d_r in pts3d_rotadas:
        pts3d_r[0] -= dif_x
        pts3d_r[1] -= dif_y

    P = np.array([
        [1, 0, 0],  # XY projection
        [0, 1, 0],
        [0, 0, 0]
    ], dtype = 'float32')

    # Apply the projection
    pts2d_proyectadas = np.dot(pts3d_rotadas, P.T)[:, :2]
    pts2d_proyectadas = np.array(pts2d_proyectadas, dtype = 'float32')
    matrix = cv2.getPerspectiveTransform(shape_to_inject, pts2d_proyectadas)

    # Transform the perspective to fit the region
    inserted_image = cv2.warpPerspective(image_to_inject, matrix, (image.shape[1], image.shape[0]), flags = cv2.INTER_NEAREST, borderMode = cv2.BORDER_TRANSPARENT)

    # Add alpha layer to image
    # TODO: This should be not 1920x1080 but dynamic
    inserted_image = np.dstack((inserted_image, np.ones((1080, 1920), dtype = np.uint8) * 255))

    # Add transparent layer to fill poly with it
    mask = np.zeros((1080, 1920), dtype = np.uint8)

    # We fill the mask with 255 values for any pixel which
    # is inside the polygon area
    cv2.fillPoly(mask, np.int32([pts2d_proyectadas]), 255)

    # We make all the other pixels that are not the polygon
    # be transparent
    inserted_image[mask != 255, 3] = 0

    cv2.imwrite(output_filename, inserted_image)

    return inserted_image

def test():
    from moviepy import CompositeVideoClip, ImageClip, concatenate_videoclips

    clips = []
    for i in range(90):
        name = f'a_test_perspc{str(i + 1)}.png'
        test_perspective(i, name)
        clips.append(ImageClip(name, duration = 1 / 60, transparent = True).with_fps(60))

    CompositeVideoClip([
        ImageClip('C:/Users/dania/Desktop/004_youtube_video.png', duration = len(clips) * 1 / 60, transparent = True).with_fps(60),
        concatenate_videoclips(clips, is_mask = True)
    ]).write_videofile('a_test_3drotz.mp4')