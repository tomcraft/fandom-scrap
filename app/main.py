import pan, datastore, util, copy, json, time
from fastapi import FastAPI, HTTPException

print("Loading block list ...")
blocks = datastore.load_block_list()
if blocks is None:
    print("Found nothing, getting it online")
    start = time.time()
    blocks = pan.read_block_list()
    print("Finished in", util.format_duration(start, time.time()), ', saving to file...')
    print('Saving to file...')
    datastore.save_block_list(blocks)
    blocks = datastore.load_block_list()
else:
    print("Loaded", len(blocks), "blocks from file")

print("Loading detailed block list ...")
detailed_blocks = datastore.load_detailed_block_list()
if detailed_blocks is None:
    print("Found nothing, getting it online")
    detailed_blocks = copy.deepcopy(blocks)
    start = time.time()
    cache_soup, cache_properties = [], {}
    for block in detailed_blocks:
        block['properties'] = pan.read_block_properties(block['url'], cache_soup, cache_properties)
    print("Finished in", util.format_duration(start, time.time()), ', saving to file...')
    print('Saving to file...')
    datastore.save_detailed_block_list(detailed_blocks)
    detailed_blocks = datastore.load_detailed_block_list()
else:
    print("Loaded", len(detailed_blocks), "detailed blocks from file")

app = FastAPI()

@app.get("/blocks")
def get_blocks(with_details: bool = False):
    return detailed_blocks if with_details else blocks

@app.get("/blocks/{id}")
def get_block_by_id(id: str):
    result = block_by_id(id)
    if result == None:
        raise HTTPException(status_code=404, detail="Block not found")
    return result

@app.get("/status")
async def status():
    return {"status": "Running"}

def block_by_id(id):
    if ':' not in id:
        id = 'minecraft:' + id
    for block in detailed_blocks:
        if block['id'] == id:
            return block
    return None