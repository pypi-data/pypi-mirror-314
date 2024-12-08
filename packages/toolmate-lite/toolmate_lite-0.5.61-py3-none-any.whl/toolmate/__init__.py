import os, sys, platform, shutil

# check python version
# requires python 3.8+; required by package 'tiktoken'
pythonVersion = sys.version_info
if pythonVersion < (3, 8):
    print("Python version higher than 3.8 is required!")
    print("Closing ...")
    exit(1)
elif pythonVersion >= (3, 13):
    print("Some features may not work with python version newer than 3.12!")

# check package path
thisFile = os.path.realpath(__file__)
packageFolder = os.path.dirname(thisFile)
package = os.path.basename(packageFolder)

# set current directory; unnecessary; conflict with API client
#if os.getcwd() != packageFolder:
#    os.chdir(packageFolder)

# create conifg.py in case it is deleted due to errors
configFile = os.path.join(packageFolder, "config.py")
if not os.path.isfile(configFile):
    open(configFile, "a", encoding="utf-8").close()

# import config module
from toolmate import config
if not hasattr(config, "isLite"):
    try:
        from lightrag import LightRAG
        config.isLite = False
    except:
        config.isLite = True
config.isTermux = True if os.path.isdir("/data/data/com.termux/files/home") and not os.getcwd().startswith("/root") else False
if config.isTermux and shutil.which("termux-share"):
    config.terminalEnableTermuxAPI = True

# set up shared configs

config.toolMateAIFolder = packageFolder
config.toolMateAIFile = os.path.join(config.toolMateAIFolder, "main.py")
if not hasattr(config, "toolMateAIName") or not config.toolMateAIName:
    config.toolMateAIName = "ToolMate AI"

if not hasattr(config, "isPipUpdated"):
    config.isPipUpdated = False

# import shared utilities
from toolmate.utils.shared_utils import *

# other initiations

config.stopSpinning = stopSpinning
config.localStorage = getLocalStorage()

from toolmate.utils.config_tools import *
config.loadConfig = loadConfig
config.setConfig = setConfig

from toolmate.utils.tool_plugins import Plugins
config.addFunctionCall = Plugins.addFunctionCall

from toolmate.utils.vlc_utils import VlcUtil
config.isVlcPlayerInstalled = VlcUtil.isVlcPlayerInstalled()

if not hasattr(config, "isPygameInstalled"):
    try:
        # hide pygame welcome message
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
        import pygame
        pygame.mixer.init()
        config.isPygameInstalled = True
    except:
        config.isPygameInstalled = False
elif not config.isPygameInstalled:
    config.usePygame = False
thisPlatform = platform.system()
config.thisPlatform = "macOS" if thisPlatform == "Darwin" else thisPlatform
if config.terminalEnableTermuxAPI:
    checkPath()
    config.open = "termux-share"
    config.thisDistro = "Android Termux"
elif thisPlatform == "Linux":
    checkPath()
    config.open = "xdg-open"
    try:
        config.thisDistro = subprocess.check_output('lsb_release -i -s', shell=True).decode('utf-8')
    except:
        config.thisDistro = ""
elif thisPlatform == "Darwin":
    checkPath()
    config.open = "open"
    config.thisDistro = ""
elif thisPlatform == "Windows":
    config.open = "start"
    config.thisDistro = ""

config.excludeConfigList = []
config.includeIpInDeviceInfoTemp = config.includeIpInDeviceInfo
config.divider = "--------------------"
config.tts = False if not config.isVlcPlayerInstalled and not config.isPygameInstalled and not config.ttsCommand and not config.elevenlabsApi else True
config.outputTextConverters = []

# save loaded configs
config.tempInterface = ""
config.saveConfig()

# environment variables
os.environ["TOKENIZERS_PARALLELISM"] = config.tokenizers_parallelism

# create shortcuts
from toolmate.utils.shortcuts import createShortcuts
createShortcuts()

# setup optional credentials
setChatGPTAPIkey()
if not config.isTermux:
    setGoogleCredentials()

# models
from ollama import list as ollama_ls

llms = {
    "llamacpp": ["llamacpp"],
    "llamacppserver": ["llamacppserver"],
    "ollama": [i.get("model") for i in ollama_ls()["models"]],
    "groq": [
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "gemma-7b-it",
        "llama-3.3-70b-versatile",
        "llama-3.2-90b-vision-preview",
        "llama-3.2-11b-vision-preview",
        "llama-3.2-3b-preview",
        "llama-3.2-1b-preview",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "llama-guard-3-8b",
        "llama3-groq-70b-8192-tool-use-preview",
        "llama3-groq-8b-8192-tool-use-preview",
    ],
    "mistral": [
        "mistral-large-latest",
        "mistral-small-latest",
        "codestral-latest",
        "ministral-8b-latest",
        "ministral-3b-latest",
        "pixtral-12b-2409",
        "open-mixtral-8x22b",
        "open-mistral-nemo",
    ],
    "xai": [
        "grok-beta",
    ],
    "googleai": [
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro"
    ],
    "vertexai": [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ],
    "chatgpt": list(chatgptTokenLimits.keys()),
    "letmedoit": list(chatgptTokenLimits.keys()),
}
# check if llama-cpp-python is installed
try:
    from llama_cpp import Llama
except:
    del llms["llamacpp"]
# check if vertexai is installed
try:
    from vertexai.generative_models import GenerativeModel
except:
    del llms["vertexai"]

# backends
backends = tuple(llms.keys())

# context
if isServerAlive("8.8.8.8", 53): # check internet connection
    g = geocoder.ip('me')
    config.country = g.country
    config.state = g.state
    config.dayOfWeek = getDayOfWeek()
else:
    config.country = config.state = config.dayOfWeek = "n/a"