from PIL import Image
import json
import sys

def get_neighbors_color(pixels, x, y):
    neighbors = set()
    for i in range(-1, 2): #set a grid of 3x3
        for j in range(-1, 2):
            if i == 0 and j == 0: #skip the center set
                continue
            if x + i < 0 or y + j < 0: #skip pixels from outer set
                continue
            
            try:
                neighbors.add(pixels[x+i, y+j])
            except IndexError:
                pass
    return neighbors

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3: #are we receiving what is expected?
        print("country_neighbors.py input [output]")
        return
    
    #NOTE: example from class, change later if not good enough 
    image = Image.open(sys.argv[1]).convert("RGB")
    pixels = image.load()
    
    if not pixels: #HOPE THIS NEVER HAPPENS RIGHT
        return
    
    #NOTE: debugg thingy
    width, height = image.size
    
    #teach the baby
    BLACK = (0, 0, 0)
    
    regions_neighbors: dict[tuple[int, int, int], set[tuple[int, int, int]]] = {} #define the data structure for region neightbors 
    for y in range(height):
        for x in range(width):
            if pixels[x, y] != BLACK:
                continue
            
            neighboring_colors = get_neighbors_color(pixels, x, y)
            neighboring_colors.discard(BLACK)
            for region in neighboring_colors:
                regions_neighbors.setdefault(region, set())
                for n_region in neighboring_colors:
                    if n_region == region:
                        continue
                    regions_neighbors[region].add(n_region)
                    
    json_out = {}
    for key, value in regions_neighbors.items():
        json_out[str(key)] = list(value)
        
    path_out = ""
    if len(sys.argv) == 3:
        path_out = sys.argv[2]
    else:
        path_out = "neighbors.json"
    
    with open(path_out, "w") as f:
        json.dump(json_out, f, indent=2)
    
    print("wrote output to: ", path_out)
    
if __name__ == "__main__":
    main()