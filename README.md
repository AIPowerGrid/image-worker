This repository allows you to set up a AI Power Grid Worker to generate, post-process or analyze images for others


# AI Power Grid Worker reGen

This repo contains the latest implementation for the AI Power Grid Worker. This will turn your graphics card(s) into a worker for the AI Power Grid where you will create images for others. You you will receive in turn earn 'kudos' which will give you priority for your own generations.

## Important Info

- **An SSD is strongly recommended** especially if you are offering more than one model.
  - If you only have an HDD available to you, you can only offer one model and will have to be able to load 3-8gb off disk within 60 seconds or the worker will not function.
- Do not set threads higher than 2 unless you have a data-center grade card (48gb+ VRAM)
- Your memory usage will increase up until the number of queued jobs (`queue_size` in the config).
  - If you have **less than 32gb of system ram**, you should should stick to `queue_size: 1`.
  - If you have **less than 16gb of system ram** or you experience frequent memory-related crashes:
    - Do not offer SDXL/SD21 models. You can do this by adding ` ALL SDXL` and `ALL SD21` to your `models_to_skip` if you are using the `TOP N` model load option to automatically remove these heavier models from your offerings.
    - Set `allow_post_processing` and `allow_controlnet` to false
    - Set `queue_size: 0`
- If you plan on running SDXL, you will need to ensure at least 9 gb of system ram remains free while the worker is running.
- If you have an 8 gb card, SDXL will only reliably work at max_power values close to 32. 42 was too high for tests on a 2080 in certain cases.

### AMD
~~Please note that **AMD cards are not currently well supported**, but may be in the future.~~

> Update: **AMD** now has been shown to have better support but for **linux machines only** - linux must be installed on the bare metal machine; windows systems, WSL or linux containers still do not work. You can now follow this guide using  `grid-bridge-rocm.sh` and `update-runtime-rocm.sh` where appropriate.

If you are willing to try with your AMD card, join the [discord discussion](https://discord.com/channels/781145214752129095/1076124012305993768).

# Installing

**Please see the prior section before proceeding.**

If you haven't already, go to [AI Power Grid and register an account](https://aigrid.net/register), then store your API key somewhere secure. Treat your API key like a password. You will need it later in these instructions. This will allow your worker to gather kudos for your account.


### Windows

#### Using git (recommended)

Use these instructions if you have installed [git for windows](https://gitforwindows.org/).

This option is recommended as it will make keeping your repository up to date much easier.

1. Open `powershell` (also referred to as terminal) or `cmd` from the start menu.

2. Using `cd`, navigate to a folder that you want the worker installed in.

   - Note that the folder you are in will create a folder named `image-worker`

3. Run the following commands within the folder chosen (the folder `image-worker` if using the example above)
    ```bash
    git clone https://github.com/AIPowerGrid/image-worker
    cd image-worker
    ```
4. Continue with the [Basic Usage](#Basic-Usage) instructions

#### Without git

Use these instructions if you do not have git for windows and do not want to install it. These instructions make updating the worker a bit more difficult down the line.

1. Download [the zipped version](https://github.com/AIPowerGrid/image-worker/archive/refs/heads/main.zip)
1. Extract it to any folder of your choice
1. Continue with the [Basic Usage](#Basic-Usage) instructions

### Linux

This assumes you have git installed

Open a bash terminal and run these commands (just copy-paste them all together)

```bash
git clone https://github.com/AIPowerGrid/image-worker
cd image-worker
```

Continue with the [Basic Usage](#basic-usage) instructions

### AMD

**AMD** now has been shown to have better support but for **linux machines only** - it's best to have linux installed directly on your machine. [WSL support](README_advanced.md#advanced-users-amd-rocm-inside-windows-wsl) is highly experimental. You can now follow this guide using  `grid-bridge-rocm.sh` and `update-runtime-rocm.sh` where appropriate.

If you are willing to try with your AMD card, join the [discord discussion](https://discord.com/channels/781145214752129095/1076124012305993768) in the [official discord](https://discord.gg/3DxrhksKzn).

## Basic Usage

### Configure

1. Make a copy of `bridgeData_template.yaml` to `bridgeData.yaml`
2. Edit `bridgeData.yaml` and follow the instructions within to fill in your details.

#### Suggested settings

Models are loaded as needed and just-in-time. You can offer as many models as you want **provided you have an SSD, at least 32gb of ram, and at least 8gb of VRAM (see [Important Info](#important-info)**. Workers with HDDs are not recommended at this time but those with HDDs should run exactly 1 model. A typical SD1.5 model is around 2gb each, while a typical SDXL model is around 7gb each. Offering `all` models is currently around 700gb total and we commit to keeping that number below 1TB with any future changes.

> Note: We suggest you disable any 'sleep' or reduced power modes for your system while the worker is running.

- If you have a **24gb+ vram card**:
  ```yaml
  - safety_on_gpu: true
  - high_memory_mode: true
  - high_performance_mode: true
  - post_process_job_overlap: true
  - unload_models_from_vram_often: false
  - max_threads: 1 # If you have Flux/Cascade loaded, otherwise 2 max
  - queue_size: 2 # You can set to 3 if you have 64GB or more of RAM
  - max_batch: 8 # or higher

- If you have a **12gb - 16gb card**:
  ```yaml
  - safety_on_gpu: true # Consider setting to `false` if offering Cascade or Flux
  - high_memory_mode: true
  - moderate_performance_mode: true
  - unload_models_from_vram_often: false
  - max_threads: 1
  - max_batch: 4 # or higher

- If you have an **8gb-10gb vram card**:
  - ```yaml
    - queue_size: 1 # max **or** only offer flux
    - safety_on_gpu: false
    - max_threads: 1
    - max_power: 32 # no higher than 32
    - max_batch: 4 # no higher than 4
    - allow_post_processing: false # If offering SDXL or Flux, otherwise you may set to true
    - allow_sdxl_controlnet: false

  - Be sure to shut every single VRAM consuming application you can and do not use the computer with the worker running for any purpose.

- Workers which have **low end cards or have low performance for other reasons**:
  - `- extra_slow_worker: true`
    - gives you considerably more time to finish job, but requests will not go to your worker unless the requester opts-in (even anon users do not use extra_slow_workers by default). You should only consider using this if you have historically had less than 0.3 MPS/S or less than 3000 kudos/hr consistently **and** you are sure the worker is otherwise configured correctly.
  - `- limit_max_steps: true`
    - reduces the maximum total number of steps in a single job you will receive based on the model baseline.
  - `- preload_timeout: 120`
    - gives you more time to load models off disk. **Note**: Abusing this value can lead to a major loss of kudos and may also lead to maintainance mode, even with `extra_slow_worker: true`.

## Updating

To update:

1. Shut down your worker by pressing `Ctrl+C` once and waiting for the worker to stop.

2. Update this repo using the appropriate method:

You can double click the provided script files below from a file explorer or run it from a terminal like `bash`, `cmd` depending on your OS. The latter option will allow you to **see errors in case of a crash**, so it's recommended.

### git method

Use this approach if you cloned the original repository using `git clone`

    1. Open a or `bash`, `cmd`, or `powershell` terminal depending on your OS
    2. Navigate to the folder you have the AI Power Grid Worker repository installed if you're not already there.
    3. run `git pull`

#### zip method

Use this approach if you downloaded the git repository as a zip file and extracted it somewhere.


    1. delete the `grid_worker_regen/` directory from your folder
    1. Download the [repository from github as a zip file](https://github.com/db0/grid-worker-reGen/archive/refs/heads/main.zip)
    1. Extract its contents into the same the folder you have the AI Power Grid Worker repository installed, overwriting any existing files


### Updating runtime
>
> **Warning**: Certain antiviruses (including Avast) have been reported to interfere with the install. If you get the error `curl: (35) schannel: next InitializeSecurityContext failed: CRYPT_E_NO_REVOCATION_CHECK` when running this file, disable your antivirus, run the file again, and then re-enable your antivirus.

4. Run the `update-runtime` script for your OS. This will update all dependencies if required.
   - Some updates may not require this and the update notification will tell you if this is the case.
   - When in doubt, you should run it anyway.
   - **Advanced users**: If you do not want to use mamba or you are comfortable with python/venvs, see [README_advanced.md](README_advanced.md).

# Custom Models

You can host your own image models on the grid which are not available in our model reference, but this process is a bit more complex.

To start with, you need to manually request the `customizer` role from then grid team. You can ask for it in the discord channel. This is a manually assigned role to prevent abuse of this feature.

Once you have the customizer role, you need to download the model files you want to host. Place them in any location on your system.

Finally, you need to point your worker to their location and provide some information about them. On your bridgeData.yaml simply add lines like the following

```
custom_models:
  - name: Movable figure model XL
    baseline: stable_diffusion_xl
    filepath: /home/db0/projects/CUSTOM_MODELS/PVCStyleModelMovable_beta25Realistic.safetensors
```

And then add the same "name" to your models_to_load.

If everything was setup correctly, you should now see a `custom_models.json` in your worker directory after the worker starts, and the model should be offered by your worker.

Note that:

* You cannot serve custom models with the same name as any of our regular models
* The grid doesn't know your model, so it will treat it as a SD 1.5 model for kudos rewards and cannot warn people using the wrong parameters such as clip_skip

# Docker

See [README_advanced.md](README_advanced.md).


# Model Usage
Many models in this project use the CreativeML OpenRAIL License.  [Please read the full license here.](https://huggingface.co/spaces/CompVis/stable-diffusion-license)
