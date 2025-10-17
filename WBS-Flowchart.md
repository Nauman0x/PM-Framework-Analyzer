# PM Framework Analyzer - WBS Flowchart

## Work Breakdown Structure - Visual Flow

This flowchart represents the complete Work Breakdown Structure for the PM Framework Analyzer project, organized in a hierarchical top-to-bottom flow.

```mermaid
flowchart TB
    Start([PM Framework Analyzer Project])
    
    Start --> Phase1[Phase 1: Planning & Design]
    Start --> Phase2[Phase 2: Development]
    Start --> Phase3[Phase 3: Quality & Deployment]
    
    Phase1 --> Init[1. PROJECT INITIATION]
    Phase1 --> Design[2. SYSTEM DESIGN]
    
    Phase2 --> Backend[3. BACKEND DEVELOPMENT]
    Phase2 --> Frontend[4. FRONTEND DEVELOPMENT]
    Phase2 --> Features[5. FEATURE IMPLEMENTATION]
    
    Phase3 --> Testing[6. TESTING]
    Phase3 --> Deploy[7. DEPLOYMENT]
    Phase3 --> Docs[8. DOCUMENTATION]
    Phase3 --> QA[9. QUALITY ASSURANCE]
    Phase3 --> Maintain[10. MAINTENANCE]

    %% Project Initiation
    Init --> Init1[1.1 Requirements Gathering]
    Init1 --> Init11[Define scope & objectives]
    Init1 --> Init12[Identify stakeholder requirements]
    Init1 --> Init13[Document functional requirements]
    Init1 --> Init14[Document non-functional requirements]
    
    Init --> Init2[1.2 Project Planning]
    Init2 --> Init21[Create project timeline]
    Init2 --> Init22[Identify required technologies]
    Init2 --> Init23[Define deliverables]
    Init2 --> Init24[Risk assessment & mitigation]

    %% System Design
    Design --> Design1[2.1 Architecture Design]
    Design1 --> Design11[Database schema - Book, Section, Page]
    Design1 --> Design12[Django MVC architecture]
    Design1 --> Design13[API integration - Gemini AI]
    Design1 --> Design14[Deployment architecture - Vercel]
    
    Design --> Design2[2.2 UI Design]
    Design2 --> Design21[Wireframes & mockups]
    Design2 --> Design22[Navigation flow design]
    Design2 --> Design23[Responsive layout planning]
    Design2 --> Design24[Color scheme & branding]
    
    Design --> Design3[2.3 Data Flow Design]
    Design3 --> Design31[PDF extraction workflow]
    Design3 --> Design32[Search & filter logic]
    Design3 --> Design33[AI analysis request/response flow]
    Design3 --> Design34[Navigation context tracking]

    %% Backend Development
    Backend --> Backend1[3.1 Django Setup]
    Backend1 --> Backend11[Initialize Django project]
    Backend1 --> Backend12[Configure settings]
    Backend1 --> Backend13[Setup virtual environment]
    Backend1 --> Backend14[Install dependencies]
    
    Backend --> Backend2[3.2 Database Development]
    Backend2 --> Backend21[Create Book model]
    Backend2 --> Backend22[Create Section model with hierarchy]
    Backend2 --> Backend23[Create Page model]
    Backend2 --> Backend24[Setup database migrations]
    Backend2 --> Backend25[Implement custom sorting - PMBOK]
    
    Backend --> Backend3[3.3 PDF Processing]
    Backend3 --> Backend31[PDF text extraction - pdfplumber]
    Backend3 --> Backend32[Section detection logic]
    Backend3 --> Backend33[Page-to-section mapping]
    Backend3 --> Backend34[Handle PDF outline/bookmarks]
    Backend3 --> Backend35[Content storage optimization]
    
    Backend --> Backend4[3.4 Data Import Commands]
    Backend4 --> Backend41[import_iso21500 command]
    Backend4 --> Backend42[import_iso21502 command]
    Backend4 --> Backend43[import_prince2 command]
    Backend4 --> Backend44[import_pmbok command]
    Backend4 --> Backend45[Error handling & validation]
    
    Backend --> Backend5[3.5 Business Logic]
    Backend5 --> Backend51[Search functionality]
    Backend5 --> Backend52[Topic comparison logic]
    Backend5 --> Backend53[Navigation tracking system]
    Backend5 --> Backend54[Content filtering & pagination]
    
    Backend --> Backend6[3.6 AI Integration]
    Backend6 --> Backend61[Setup Gemini API client]
    Backend6 --> Backend62[Design AI analysis prompts]
    Backend6 --> Backend63[Implement content preparation]
    Backend6 --> Backend64[Build response parsing logic]
    Backend6 --> Backend65[Create markdown-to-HTML formatter]
    Backend6 --> Backend66[Error handling for API calls]

    %% Frontend Development
    Frontend --> Frontend1[4.1 Template Development]
    Frontend1 --> Frontend11[Base template layout]
    Frontend1 --> Frontend12[Index/home page]
    Frontend1 --> Frontend13[Book detail page]
    Frontend1 --> Frontend14[Section detail view]
    Frontend1 --> Frontend15[Search results page]
    Frontend1 --> Frontend16[Compare page]
    Frontend1 --> Frontend17[Analysis loading page]
    Frontend1 --> Frontend18[Analysis results page]
    
    Frontend --> Frontend2[4.2 Styling & UI]
    Frontend2 --> Frontend21[Gradient color scheme]
    Frontend2 --> Frontend22[Card-based layouts]
    Frontend2 --> Frontend23[Responsive navigation]
    Frontend2 --> Frontend24[Form styling]
    Frontend2 --> Frontend25[Hover effects & transitions]
    Frontend2 --> Frontend26[Loading spinners & indicators]
    
    Frontend --> Frontend3[4.3 Interactive Features]
    Frontend3 --> Frontend31[Search form with validation]
    Frontend3 --> Frontend32[Topic analysis buttons]
    Frontend3 --> Frontend33[Smart back navigation]
    Frontend3 --> Frontend34[Context-aware breadcrumbs]
    Frontend3 --> Frontend35[Auto-submit loading page]
    
    Frontend --> Frontend4[4.4 Accessibility & UX]
    Frontend4 --> Frontend41[Keyboard navigation]
    Frontend4 --> Frontend42[Screen reader compatibility]
    Frontend4 --> Frontend43[Clear error messaging]
    Frontend4 --> Frontend44[Loading state indicators]
    Frontend4 --> Frontend45[Mobile responsiveness]

    %% Feature Implementation
    Features --> Features1[5.1 Book Management]
    Features1 --> Features11[List all books]
    Features1 --> Features12[Display book metadata]
    Features1 --> Features13[Hierarchical table of contents]
    Features1 --> Features14[Section navigation]
    
    Features --> Features2[5.2 Search Functionality]
    Features2 --> Features21[Topic search across books]
    Features2 --> Features22[Results grouped by book]
    Features2 --> Features23[Display page numbers & info]
    Features2 --> Features24[Empty query validation]
    Features2 --> Features25[No results handling]
    
    Features --> Features3[5.3 Compare Feature]
    Features3 --> Features31[Recommended topics display]
    Features3 --> Features32[Search input on compare page]
    Features3 --> Features33[Link to analysis feature]
    Features3 --> Features34[Validation for empty searches]
    
    Features --> Features4[5.4 AI Analysis Feature]
    Features4 --> Features41[Loading page with progress]
    Features4 --> Features42[Generate comparative analysis]
    Features4 --> Features43[Format analysis output]
    Features4 --> Features44[Display similarities section]
    Features4 --> Features45[Display differences section]
    Features4 --> Features46[Display unique points section]
    Features4 --> Features47[Show analyzed topics list]
    Features4 --> Features48[Include page references]
    
    Features --> Features5[5.5 Navigation System]
    Features5 --> Features51[Context tracking - from parameter]
    Features5 --> Features52[Smart back buttons]
    Features5 --> Features53[Return to analysis from topics]
    Features5 --> Features54[Breadcrumb navigation]
    Features5 --> Features55[Direct section linking]

    %% Testing
    Testing --> Testing1[6.1 Unit Testing]
    Testing1 --> Testing11[Model tests]
    Testing1 --> Testing12[View logic tests]
    Testing1 --> Testing13[PDF extraction tests]
    Testing1 --> Testing14[Search functionality tests]
    Testing1 --> Testing15[Markdown formatting tests]
    
    Testing --> Testing2[6.2 Integration Testing]
    Testing2 --> Testing21[End-to-end search workflow]
    Testing2 --> Testing22[AI analysis integration]
    Testing2 --> Testing23[Navigation flow testing]
    Testing2 --> Testing24[Database query optimization]
    
    Testing --> Testing3[6.3 User Acceptance Testing]
    Testing3 --> Testing31[Search accuracy validation]
    Testing3 --> Testing32[AI analysis quality review]
    Testing3 --> Testing33[UI/UX feedback collection]
    Testing3 --> Testing34[Performance benchmarking]
    
    Testing --> Testing4[6.4 Browser Testing]
    Testing4 --> Testing41[Chrome compatibility]
    Testing4 --> Testing42[Firefox compatibility]
    Testing4 --> Testing43[Safari compatibility]
    Testing4 --> Testing44[Edge compatibility]
    Testing4 --> Testing45[Mobile browser testing]

    %% Deployment
    Deploy --> Deploy1[7.1 Environment Configuration]
    Deploy1 --> Deploy11[Create .env file structure]
    Deploy1 --> Deploy12[Setup environment variables]
    Deploy1 --> Deploy13[Configure Django secret key]
    Deploy1 --> Deploy14[Setup Gemini API key]
    Deploy1 --> Deploy15[Configure debug settings]
    
    Deploy --> Deploy2[7.2 Security Implementation]
    Deploy2 --> Deploy21[Secure API keys - env variables]
    Deploy2 --> Deploy22[Configure ALLOWED_HOSTS]
    Deploy2 --> Deploy23[Setup CSRF protection]
    Deploy2 --> Deploy24[Implement SSL/HTTPS settings]
    Deploy2 --> Deploy25[Configure security headers]
    
    Deploy --> Deploy3[7.3 Vercel Configuration]
    Deploy3 --> Deploy31[Create vercel.json]
    Deploy3 --> Deploy32[Setup build script]
    Deploy3 --> Deploy33[Configure Python runtime]
    Deploy3 --> Deploy34[Setup routing rules]
    Deploy3 --> Deploy35[Configure static files]
    
    Deploy --> Deploy4[7.4 Database Preparation]
    Deploy4 --> Deploy41[Run all migrations]
    Deploy4 --> Deploy42[Import ISO 21500 - 23 sections]
    Deploy4 --> Deploy43[Import ISO 21502 - 142 sections]
    Deploy4 --> Deploy44[Import PRINCE2 - 302 sections]
    Deploy4 --> Deploy45[Import PMBOK - 192 sections]
    Deploy4 --> Deploy46[Verify data integrity - 667 sections]
    
    Deploy --> Deploy5[7.5 Deployment Execution]
    Deploy5 --> Deploy51[Install Vercel CLI]
    Deploy5 --> Deploy52[Authenticate with Vercel]
    Deploy5 --> Deploy53[Initialize Git repository]
    Deploy5 --> Deploy54[Connect to GitHub]
    Deploy5 --> Deploy55[Set env variables in Vercel]
    Deploy5 --> Deploy56[Deploy to production]
    Deploy5 --> Deploy57[Configure deployment protection]
    
    Deploy --> Deploy6[7.6 Post-Deployment]
    Deploy6 --> Deploy61[Verify URL accessibility]
    Deploy6 --> Deploy62[Test all features in production]
    Deploy6 --> Deploy63[Monitor error logs]
    Deploy6 --> Deploy64[Performance optimization]
    Deploy6 --> Deploy65[Setup custom domain - optional]

    %% Documentation
    Docs --> Docs1[8.1 Technical Documentation]
    Docs1 --> Docs11[Create README.md]
    Docs1 --> Docs12[Write deployment guide]
    Docs1 --> Docs13[Document API integration]
    Docs1 --> Docs14[Code comments & docstrings]
    Docs1 --> Docs15[Database schema documentation]
    
    Docs --> Docs2[8.2 User Documentation]
    Docs2 --> Docs21[User guide - search]
    Docs2 --> Docs22[Instructions - AI analysis]
    Docs2 --> Docs23[Navigation guide]
    Docs2 --> Docs24[FAQ section]
    
    Docs --> Docs3[8.3 Project Documentation]
    Docs3 --> Docs31[Work Breakdown Structure]
    Docs3 --> Docs32[WBS Flowchart]
    Docs3 --> Docs33[Project timeline]
    Docs3 --> Docs34[Technology stack docs]

    %% Quality Assurance
    QA --> QA1[9.1 Code Quality]
    QA1 --> QA11[Code review & refactoring]
    QA1 --> QA12[PEP 8 compliance]
    QA1 --> QA13[Remove code duplication]
    QA1 --> QA14[Optimize database queries]
    QA1 --> QA15[Error handling improvements]
    
    QA --> QA2[9.2 Performance Optimization]
    QA2 --> QA21[Database indexing]
    QA2 --> QA22[Query optimization]
    QA2 --> QA23[Static file caching]
    QA2 --> QA24[Lazy loading implementation]
    QA2 --> QA25[Content compression]
    
    QA --> QA3[9.3 Security Audit]
    QA3 --> QA31[Vulnerability scanning]
    QA3 --> QA32[Dependency updates]
    QA3 --> QA33[SQL injection prevention]
    QA3 --> QA34[XSS protection verification]
    QA3 --> QA35[CSRF token validation]

    %% Maintenance
    Maintain --> Maintain1[10.1 Monitoring]
    Maintain1 --> Maintain11[Setup error tracking]
    Maintain1 --> Maintain12[Monitor API usage & limits]
    Maintain1 --> Maintain13[Track deployment performance]
    Maintain1 --> Maintain14[User analytics - optional]
    
    Maintain --> Maintain2[10.2 Updates & Enhancements]
    Maintain2 --> Maintain21[Django framework updates]
    Maintain2 --> Maintain22[Dependency updates]
    Maintain2 --> Maintain23[Security patches]
    Maintain2 --> Maintain24[Feature enhancements]
    Maintain2 --> Maintain25[Bug fixes]
    
    Maintain --> Maintain3[10.3 Backup & Recovery]
    Maintain3 --> Maintain31[Database backup strategy]
    Maintain3 --> Maintain32[Code repository management]
    Maintain3 --> Maintain33[Disaster recovery plan]
    Maintain3 --> Maintain34[Version control best practices]

    %% Completion
    Deploy6 --> Complete([Project Complete<br/>Status: DEPLOYED<br/>667 Sections Imported<br/>4 PM Standards])
    Docs3 --> Complete
    QA3 --> Complete
    Maintain3 --> Complete
    
    %% Styling
    style Start fill:#667eea,stroke:#764ba2,stroke-width:4px,color:#fff
    style Complete fill:#27ae60,stroke:#229954,stroke-width:4px,color:#fff
    
    style Phase1 fill:#e8eaf6,stroke:#667eea,stroke-width:3px
    style Phase2 fill:#fff9e6,stroke:#e67e22,stroke-width:3px
    style Phase3 fill:#e6f7ff,stroke:#3498db,stroke-width:3px
    
    style Init fill:#f0f4ff,stroke:#667eea,stroke-width:2px
    style Design fill:#f0f4ff,stroke:#667eea,stroke-width:2px
    style Backend fill:#fff9e6,stroke:#e67e22,stroke-width:2px
    style Frontend fill:#fff9e6,stroke:#e67e22,stroke-width:2px
    style Features fill:#fff9e6,stroke:#e67e22,stroke-width:2px
    style Testing fill:#e6f7ff,stroke:#3498db,stroke-width:2px
    style Deploy fill:#e6f7ff,stroke:#3498db,stroke-width:2px
    style Docs fill:#e6f7ff,stroke:#3498db,stroke-width:2px
    style QA fill:#e6f7ff,stroke:#3498db,stroke-width:2px
    style Maintain fill:#e6f7ff,stroke:#3498db,stroke-width:2px
```

## Flowchart Legend

### Node Types
- **Oval Shapes**: Project start and completion milestones
- **Rectangles**: Work packages and tasks
- **Rounded Rectangles**: Phase groupings

### Color Coding
- **Purple Gradient**: Project boundaries (Start/Complete)
- **Light Purple**: Phase 1 - Planning & Design
- **Light Orange**: Phase 2 - Development
- **Light Blue**: Phase 3 - Quality & Deployment
- **Green**: Project completion

### Project Phases

**Phase 1: Planning & Design**
- Project Initiation
- System Design

**Phase 2: Development**
- Backend Development
- Frontend Development
- Feature Implementation

**Phase 3: Quality & Deployment**
- Testing
- Deployment
- Documentation
- Quality Assurance
- Maintenance & Support

### Project Metrics
- **Total Work Packages**: 10 major phases
- **Total Tasks**: 200+ individual tasks
- **Total Sections Imported**: 667 sections
- **PM Standards Covered**: 4 (ISO 21500, ISO 21502, PRINCE2, PMBOK)
- **Development Approach**: Agile/Iterative

**Last Updated**: October 5, 2025  
**Project Status**: COMPLETED AND DEPLOYED

---

## Simplified Project Flow

```mermaid
graph LR
    A[Start Project] --> B[Plan & Design]
    B --> C[Develop Backend]
    C --> D[Develop Frontend]
    D --> E[Implement Features]
    E --> F[Test Everything]
    F --> G[Deploy to Vercel]
    G --> H[Monitor & Maintain]
    
    style A fill:#667eea,color:#fff
    style H fill:#27ae60,color:#fff
    style G fill:#e67e22,color:#fff
```

## Feature Development Flow

```mermaid
flowchart LR
    A[User Needs] --> B{Feature Type?}
    B -->|Search| C[Search Implementation]
    B -->|Compare| D[Compare Implementation]
    B -->|AI Analysis| E[AI Integration]
    
    C --> F[Search across books]
    C --> G[Group by book]
    C --> H[Display results]
    
    D --> I[Recommended topics]
    D --> J[Search input]
    D --> K[Link to analysis]
    
    E --> L[Loading page]
    E --> M[Call Gemini API]
    E --> N[Format response]
    E --> O[Display insights]
    
    H --> P[User views topics]
    K --> P
    O --> P
    P --> Q[Navigate back smartly]
    
    style A fill:#667eea,color:#fff
    style B fill:#e67e22,color:#fff
    style P fill:#27ae60,color:#fff
```

## Data Flow Diagram

```mermaid
flowchart TD
    PDF[PDF Files] --> Extract[PDF Extraction]
    Extract --> Parse[Parse Sections]
    Parse --> DB[(SQLite Database)]
    
    DB --> Books[Books Table]
    DB --> Sections[Sections Table]
    DB --> Pages[Pages Table]
    
    User[User Input] --> Search{Search Query}
    Search --> Query[Query Database]
    Query --> Results[Display Results]
    
    Search --> AI{AI Analysis?}
    AI -->|Yes| Prepare[Prepare Content]
    Prepare --> Gemini[Gemini API]
    Gemini --> Format[Format Response]
    Format --> Display[Display Analysis]
    
    AI -->|No| Results
    
    style PDF fill:#e74c3c,color:#fff
    style DB fill:#3498db,color:#fff
    style Gemini fill:#9b59b6,color:#fff
    style Display fill:#27ae60,color:#fff
```

## Deployment Pipeline

```mermaid
flowchart LR
    A[Local Development] --> B[Git Commit]
    B --> C[Push to GitHub]
    C --> D[Vercel Detection]
    D --> E[Build Process]
    E --> F{Build Success?}
    F -->|Yes| G[Deploy to Production]
    F -->|No| H[Show Errors]
    G --> I[Set Environment Vars]
    I --> J[Configure Protection]
    J --> K[Live Application]
    H --> A
    
    style A fill:#3498db,color:#fff
    style K fill:#27ae60,color:#fff
    style H fill:#e74c3c,color:#fff
    style G fill:#e67e22,color:#fff
```

## Usage Flow

```mermaid
stateDiagram-v2
    [*] --> HomePage
    HomePage --> BookDetail: Click Book
    HomePage --> Search: Enter Search
    HomePage --> Compare: Go to Compare
    
    BookDetail --> SectionView: Click Section
    SectionView --> BookDetail: Back
    
    Search --> SearchResults: View Results
    SearchResults --> SectionView: Click Topic
    SearchResults --> AIAnalysis: Click Analysis
    
    Compare --> Search: Search Topic
    Compare --> AIAnalysis: Click Analysis
    
    AIAnalysis --> LoadingPage: Processing
    LoadingPage --> AnalysisResults: Complete
    AnalysisResults --> SectionView: Click Reference
    SectionView --> AnalysisResults: Back to Analysis
    
    SectionView --> [*]
    AnalysisResults --> [*]
```

---

## How to View These Diagrams

These flowcharts use Mermaid syntax. To view them:

1. **GitHub**: Automatically renders on GitHub when you view this file
2. **VS Code**: Install "Markdown Preview Mermaid Support" extension
3. **Online**: Copy the mermaid code to https://mermaid.live/
4. **Export**: Use mermaid.live to export as PNG, SVG, or PDF

---

**Created:** October 5, 2025  
**Project:** PM Framework Analyzer  
**Version:** 1.0

## Simplified Project Flow

```mermaid
graph LR
    A[Start Project] --> B[Plan & Design]
    B --> C[Develop Backend]
    C --> D[Develop Frontend]
    D --> E[Implement Features]
    E --> F[Test Everything]
    F --> G[Deploy to Vercel]
    G --> H[Monitor & Maintain]
    
    style A fill:#667eea,color:#fff
    style H fill:#27ae60,color:#fff
    style G fill:#e67e22,color:#fff
```

## Feature Development Flow

```mermaid
flowchart LR
    A[User Needs] --> B{Feature Type?}
    B -->|Search| C[Search Implementation]
    B -->|Compare| D[Compare Implementation]
    B -->|AI Analysis| E[AI Integration]
    
    C --> F[Search across books]
    C --> G[Group by book]
    C --> H[Display results]
    
    D --> I[Recommended topics]
    D --> J[Search input]
    D --> K[Link to analysis]
    
    E --> L[Loading page]
    E --> M[Call Gemini API]
    E --> N[Format response]
    E --> O[Display insights]
    
    H --> P[User views topics]
    K --> P
    O --> P
    P --> Q[Navigate back smartly]
    
    style A fill:#667eea,color:#fff
    style B fill:#e67e22,color:#fff
    style P fill:#27ae60,color:#fff
```

## Data Flow Diagram

```mermaid
flowchart TD
    PDF[PDF Files] --> Extract[PDF Extraction]
    Extract --> Parse[Parse Sections]
    Parse --> DB[(SQLite Database)]
    
    DB --> Books[Books Table]
    DB --> Sections[Sections Table]
    DB --> Pages[Pages Table]
    
    User[User Input] --> Search{Search Query}
    Search --> Query[Query Database]
    Query --> Results[Display Results]
    
    Search --> AI{AI Analysis?}
    AI -->|Yes| Prepare[Prepare Content]
    Prepare --> Gemini[Gemini API]
    Gemini --> Format[Format Response]
    Format --> Display[Display Analysis]
    
    AI -->|No| Results
    
    style PDF fill:#e74c3c,color:#fff
    style DB fill:#3498db,color:#fff
    style Gemini fill:#9b59b6,color:#fff
    style Display fill:#27ae60,color:#fff
```

## Deployment Pipeline

```mermaid
flowchart LR
    A[Local Development] --> B[Git Commit]
    B --> C[Push to GitHub]
    C --> D[Vercel Detection]
    D --> E[Build Process]
    E --> F{Build Success?}
    F -->|Yes| G[Deploy to Production]
    F -->|No| H[Show Errors]
    G --> I[Set Environment Vars]
    I --> J[Configure Protection]
    J --> K[Live Application]
    H --> A
    
    style A fill:#3498db,color:#fff
    style K fill:#27ae60,color:#fff
    style H fill:#e74c3c,color:#fff
    style G fill:#e67e22,color:#fff
```

## Usage Flow

```mermaid
stateDiagram-v2
    [*] --> HomePage
    HomePage --> BookDetail: Click Book
    HomePage --> Search: Enter Search
    HomePage --> Compare: Go to Compare
    
    BookDetail --> SectionView: Click Section
    SectionView --> BookDetail: Back
    
    Search --> SearchResults: View Results
    SearchResults --> SectionView: Click Topic
    SearchResults --> AIAnalysis: Click Analysis
    
    Compare --> Search: Search Topic
    Compare --> AIAnalysis: Click Analysis
    
    AIAnalysis --> LoadingPage: Processing
    LoadingPage --> AnalysisResults: Complete
    AnalysisResults --> SectionView: Click Reference
    SectionView --> AnalysisResults: Back to Analysis
    
    SectionView --> [*]
    AnalysisResults --> [*]
```

---

## How to View These Diagrams

These flowcharts use Mermaid syntax. To view them:

1. **GitHub**: Automatically renders on GitHub when you view this file
2. **VS Code**: Install "Markdown Preview Mermaid Support" extension
3. **Online**: Copy the mermaid code to https://mermaid.live/
4. **Export**: Use mermaid.live to export as PNG, SVG, or PDF

---

**Created:** October 5, 2025  
**Project:** PM Framework Analyzer  
**Version:** 1.0
