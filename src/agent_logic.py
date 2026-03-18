import os
from typing import Annotated, TypedDict, List, Dict, Any, Literal
import logging
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from src.prompts import (
    CLAUSE_ANALYZER_SYSTEM,
    RISK_IDENTIFIER_SYSTEM,
    SELF_CORRECTION_SYSTEM,
