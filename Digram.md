flowchart TD
    A[API Input - JSON Query] --> B[Chatbot]
    B --> C[AI Generated Response]
    C --> D[Debug and Convert AI Output Function]
    D --> E[Robust LLM2 Dictionary]
    E --> F[Final Dictionary with Features & Values]
    
    F --> G[Machine Learning Pipeline]
    G --> H[Generate Features Function]
    H --> I[Feature Engineering - Create & Validate Features]
    I --> J[Model Pipeline]
    
    J --> K[Preprocessor]
    K --> L[Imputer - Numerical Features]
    K --> M[Encoder - Categorical Features]
    
    L --> N[Classifier]
    M --> N
    N --> O[Prediction]
    
    I --> P[Get Factors Function]
    O --> P
    P --> Q[Reasons for Churn/No Churn]
    
    Q --> R[Chatbot with Prompt]
    R --> S[AI Response - Detailed Reasons]
    S --> T[API Final Output]
    
    style A fill:#e1f5fe
    style T fill:#c8e6c9
    style O fill:#fff3e0
    style G fill:#f3e5f5
    style J fill:#fce4ec