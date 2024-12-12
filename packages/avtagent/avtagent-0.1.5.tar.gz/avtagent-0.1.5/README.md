
# Agent library

## Agent library for Avnet GAI - powered by autogen

this is the customized agent library for:  
    1. security checking agent  
    2. retrieval agent  
    3. eamil writer agent  
    4. general agent  
    5. tool executor agent  

# 1. agent 
    #- config
    agent instance needs to read env. config, make sure the following config entries have been setup before creating agent
    model = os.environ.get("AZURE_OPENAI_MODEL_NAME")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    base_url = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_type = os.environ.get("OPENAI_API_TYPE")
    api_version = os.environ.get("OPENAI_API_VERSION")
        
    #- sample
    


    #import 
    from avtagent.agents import security_agent,tool_executor_agent,retrieval_agent,writer_agent,assistant_agent,group_manager_agent
    
    assistant_ag = assistant_agent()
    security_ag =  security_agent()
    retrieval_ag = retrieval_agent()
    writer_ag = writer_agent()
    writer_executor_proxy_ag =  tool_executor_agent()

