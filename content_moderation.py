"""
Content Moderation System

A system that uses AI to pre-screen user-generated content
and requires human confirmation before taking down potentially controversial posts.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from llama_index.core.workflow import (
    InputRequiredEvent,
    HumanResponseEvent
)

# Define violation categories
class ViolationCategory(str, Enum):
    HARASSMENT = "harassment"
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    NUDITY = "nudity"
    SPAM = "spam"
    MISINFORMATION = "misinformation"
    SELF_HARM = "self_harm"
    COPYRIGHT = "copyright"
    NONE = "none"

# Define severity levels
class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Define moderation decision
class ModerationDecision(str, Enum):
    APPROVE = "approve"
    FLAG_FOR_REVIEW = "flag_for_review"
    REMOVE = "remove"
    WARN = "warn"
    RESTRICT = "restrict"

# Initialize the LLM
def init_llm():
    """Initialize the LLM with appropriate parameters"""
    llm = OpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    return llm

# Function to generate mock content data
def get_mock_content():
    """Generate mock content data for testing"""
    content_items = [
        {
            "content_id": "POST-001",
            "user_id": "USER-12345",
            "content_type": "text_post",
            "text": "I love this platform! The community here is so supportive and kind.",
            "media_urls": [],
            "timestamp": datetime.now().isoformat(),
            "platform": "Social Media Platform",
            "context": "Public post on user's profile",
            "violation_category": None,
            "severity_level": None,
            "ai_confidence": None,
            "moderation_decision": None,
            "moderator_notes": None,
            "moderated_by": None,
            "moderation_date": None
        },
        {
            "content_id": "POST-002",
            "user_id": "USER-67890",
            "content_type": "text_post",
            "text": "This politician is completely corrupt and anyone who supports them is an idiot who deserves what's coming to them.",
            "media_urls": [],
            "timestamp": datetime.now().isoformat(),
            "platform": "Social Media Platform",
            "context": "Comment on a news article",
            "violation_category": None,
            "severity_level": None,
            "ai_confidence": None,
            "moderation_decision": None,
            "moderator_notes": None,
            "moderated_by": None,
            "moderation_date": None
        },
        {
            "content_id": "POST-003",
            "user_id": "USER-54321",
            "content_type": "image_post",
            "text": "Check out my new artwork!",
            "media_urls": ["https://example.com/potentially-questionable-image.jpg"],
            "timestamp": datetime.now().isoformat(),
            "platform": "Social Media Platform",
            "context": "Public post in art community",
            "violation_category": None,
            "severity_level": None,
            "ai_confidence": None,
            "moderation_decision": None,
            "moderator_notes": None,
            "moderated_by": None,
            "moderation_date": None
        }
    ]
    return content_items

# Function to get mock user data
def get_mock_user(user_id):
    """Generate mock user data"""
    users = {
        "USER-12345": {
            "user_id": "USER-12345",
            "username": "GoodUser123",
            "account_age_days": 732,
            "previous_violations": 0,
            "karma_score": 950,
            "is_verified": True,
            "follower_count": 87,
            "role": "regular"
        },
        "USER-67890": {
            "user_id": "USER-67890",
            "username": "PoliticalRanter42",
            "account_age_days": 45,
            "previous_violations": 2,
            "karma_score": 120,
            "is_verified": False,
            "follower_count": 23,
            "role": "regular"
        },
        "USER-54321": {
            "user_id": "USER-54321",
            "username": "ArtisticSoul99",
            "account_age_days": 365,
            "previous_violations": 1,
            "karma_score": 480,
            "is_verified": False,
            "follower_count": 213,
            "role": "creator"
        }
    }
    return users.get(user_id, {
        "user_id": user_id,
        "username": "UnknownUser",
        "account_age_days": 0,
        "previous_violations": 0,
        "karma_score": 0,
        "is_verified": False,
        "follower_count": 0,
        "role": "regular"
    })

# Function to analyze content for policy violations
def analyze_content_mock(content, user):
    """Analyze content for potential policy violations using mock responses"""
    
    # For a real implementation, we would call the LLM here
    # But for this example, we'll use mock responses based on content_id
    if content['content_id'] == "POST-001":
        return {
            "violation_category": "none",
            "severity_level": "low",
            "ai_confidence": 0.95,
            "recommended_action": "approve",
            "explanation": "This content is positive and does not violate any policies. It promotes a healthy community environment."
        }
    elif content['content_id'] == "POST-002":
        return {
            "violation_category": "harassment",
            "severity_level": "medium",
            "ai_confidence": 0.85,
            "recommended_action": "flag_for_review",
            "explanation": "This content contains potentially harassing language and insults directed at a group of people. While it's in a political context which may allow for some heated discussion, the personal attacks cross into harassment territory. Human review recommended due to political context."
        }
    elif content['content_id'] == "POST-003":
        return {
            "violation_category": "nudity",
            "severity_level": "high",
            "ai_confidence": 0.75,
            "recommended_action": "flag_for_review",
            "explanation": "The post text itself is fine, but the image URL suggests potentially inappropriate content. Since this is artistic work, and context matters greatly for artistic nudity, human review is recommended."
        }
    else:
        return {
            "violation_category": "none",
            "severity_level": "low",
            "ai_confidence": 0.9,
            "recommended_action": "approve",
            "explanation": "No policy violations detected in this content."
        }

# Tool function for human confirmation of content moderation decisions
async def confirm_moderation(ctx: Context, 
                           content_id: str, 
                           content_text: str,
                           username: str,
                           violation_category: str,
                           severity_level: str,
                           explanation: str,
                           moderator_name: str) -> str:
    """Request human confirmation for content moderation actions"""
    
    # Prepare the confirmation message with clear formatting
    confirmation_text = f"""
    CONTENT MODERATION REVIEW REQUIRED
    
    Content ID: {content_id}
    Posted by: {username}
    
    CONTENT TEXT:
    "{content_text}"
    
    AI ASSESSMENT:
    - Violation Category: {violation_category.upper()}
    - Severity Level: {severity_level.upper()}
    
    AI EXPLANATION:
    {explanation}
    
    THIS CONTENT REQUIRES HUMAN REVIEW BEFORE TAKING ACTION.
    """
    
    # Emit an event to the external stream to be captured
    ctx.write_event_to_stream(
        InputRequiredEvent(
            prefix=confirmation_text + f"\n\n{moderator_name}, what action should be taken? (approve/warn/restrict/remove):",
            user_name=moderator_name,
        )
    )
    
    # Wait until we see a HumanResponseEvent
    response = await ctx.wait_for_event(
        HumanResponseEvent, requirements={"user_name": moderator_name}
    )
    
    # Act on the input from the event
    user_response = response.response.strip().lower()
    
    if user_response == "approve":
        return f"Content {content_id} has been approved by {moderator_name}."
    elif user_response == "warn":
        return f"Content {content_id} has been approved with a warning to the user by {moderator_name}."
    elif user_response == "restrict":
        return f"Content {content_id} has been restricted (limited visibility) by {moderator_name}."
    elif user_response == "remove":
        return f"Content {content_id} has been removed by {moderator_name}."
    else:
        return f"Content {content_id} requires further review. Action deferred by {moderator_name}."

# Create the content moderation workflow
def create_workflow(llm):
    """Create the agent workflow for content moderation"""
    
    workflow = AgentWorkflow.from_tools_or_functions(
        [confirm_moderation],
        llm=llm,
        system_prompt="""
        You are a Content Moderation Assistant AI.
        Your role is to help human moderators review potentially problematic content.
        You MUST use the confirm_moderation function for ANY content flagged with potential policy violations.
        Never make final decisions on borderline content without human input.
        
        When content has policy violations:
        1. Clearly explain the potential violation
        2. Use the confirm_moderation function to get moderator approval
        3. Report back the final decision
        """
    )
    
    return workflow

# Main function to run the content moderation system
async def main():
    # Initialize LLM
    llm = init_llm()
    
    # Create workflow
    workflow = create_workflow(llm)
    
    # Get mock data
    content_items = get_mock_content()
    moderator_name = "Senior Moderator Johnson"
    
    print(f"Processing {len(content_items)} content items...\n")
    
    # Process each content item
    for content in content_items:
        print(f"Analyzing content: {content['content_id']}")
        print(f"Type: {content['content_type']}")
        print(f"Text: \"{content['text']}\"")
        
        # Get user info
        user = get_mock_user(content['user_id'])
        
        # Analyze content
        print("\nAnalyzing for policy violations...")
        analysis = analyze_content_mock(content, user)
        
        # Update content with analysis results
        content['violation_category'] = analysis['violation_category']
        content['severity_level'] = analysis['severity_level']
        content['ai_confidence'] = analysis['ai_confidence']
        
        print(f"Analysis complete:")
        print(f"- Violation Category: {content['violation_category']}")
        print(f"- Severity Level: {content['severity_level']}")
        print(f"- AI Confidence: {content['ai_confidence']}")
        print(f"- Recommended Action: {analysis['recommended_action']}")
        
        # For content with no violations, auto-approve
        if content['violation_category'] == 'none':
            print(f"\nNo violations detected. Auto-approving...")
            content["moderation_decision"] = "approve"
            content["moderator_notes"] = "Auto-approved by AI system"
            content["moderated_by"] = "AI System"
            content["moderation_date"] = datetime.now().isoformat()
            print(f"Content {content['content_id']} has been automatically approved.")
            continue
        
        # For content with potential violations, use the workflow approach
        print(f"\nPotential violation detected. Requesting human review...")
        
        # Use the workflow to handle the moderation process
        user_msg = f"""
        Review this content for potential {content['violation_category']} violation:
        
        Content Type: {content['content_type']}
        Text: "{content['text']}"
        
        The AI system has flagged this content with {content['severity_level']} severity.
        Please use the confirm_moderation function to get human moderator input.
        """
        
        # Run the workflow
        handler = workflow.run(
            user_msg=user_msg,
            context_dict={
                "content_id": content['content_id'],
                "content_text": content['text'],
                "username": user['username'],
                "violation_category": content['violation_category'],
                "severity_level": content['severity_level'],
                "explanation": analysis['explanation'],
                "moderator_name": moderator_name
            }
        )
        
        # Process events from the agent (this is the critical part for human input)
        async for event in handler.stream_events():
            # Handle InputRequiredEvent events (human moderator confirmation)
            if isinstance(event, InputRequiredEvent):
                print("\n" + event.prefix)
                response = input()
                handler.ctx.send_event(
                    HumanResponseEvent(
                        response=response,
                        user_name=event.user_name,
                    )
                )
        
        # Get and print the response
        response = await handler
        print(f"\nModeration result: {response}")
        
        # Update content based on human decision
        if "approved with a warning" in str(response).lower():
            content["moderation_decision"] = "warn"
        elif "approved" in str(response).lower():
            content["moderation_decision"] = "approve"
        elif "restricted" in str(response).lower():
            content["moderation_decision"] = "restrict"
        elif "removed" in str(response).lower():
            content["moderation_decision"] = "remove"
        else:
            content["moderation_decision"] = "flag_for_review"
            
        content["moderator_notes"] = "Reviewed by human moderator"
        content["moderated_by"] = moderator_name
        content["moderation_date"] = datetime.now().isoformat()
    
    # Generate moderation report
    print("\n===== CONTENT MODERATION SUMMARY =====")
    for content in content_items:
        decision = content.get('moderation_decision', 'PENDING')
        print(f"- {content['content_id']} (by {get_mock_user(content['user_id'])['username']}): {decision.upper()}")
        print(f"  Type: {content['content_type']}")
        print(f"  Text: \"{content['text'][:50]}{'...' if len(content['text']) > 50 else ''}\"")
        if content.get('violation_category') and content['violation_category'] != 'none':
            print(f"  Violation: {content['violation_category']} ({content['severity_level']})")
        print(f"  Moderated by: {content.get('moderated_by', 'N/A')}")
        print(f"  Moderation date: {content.get('moderation_date', 'N/A')}")
        print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
