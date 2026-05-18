import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "prepsprint_secure_matrix_vault_770X")

# 🗄️ COMPLETE TECHNICAL QUESTION BANK (5 QUESTIONS PER SKILL)
QUESTIONS_DB = {
    "python": [
        {"q": "Explain the architectural difference between Python's Global Interpreter Lock (GIL) and multiprocessing for CPU-bound tasks.", "keywords": ["gil", "cpu", "multiprocessing", "thread", "parallel"]},
        {"q": "How do Python decorators modify function behavior at runtime? Provide structural context.", "keywords": ["decorator", "wrapper", "runtime", "closure", "arguments"]},
        {"q": "Explain how Python's memory management handles reference counting and cyclical garbage collection.", "keywords": ["reference counting", "garbage collection", "cyclical", "generation", "gc"]},
        {"q": "Describe the difference between dunder methods __new__ and __init__ during object instantiation.", "keywords": ["__new__", "__init__", "instantiation", "metaclass", "allocates"]},
        {"q": "How do Python generators optimize memory footprint using lazy evaluation via the yield keyword?", "keywords": ["generator", "yield", "lazy evaluation", "memory", "iterator"]}
    ],
    "javascript": [
        {"q": "Analyze how the JavaScript Event Loop manages the Call Stack, Web APIs, Task Queue, and Microtask Queue.", "keywords": ["event loop", "stack", "queue", "microtask", "promise"]},
        {"q": "What is the structural difference between classical prototypical inheritance and closures for encapsulation in JS?", "keywords": ["prototype", "closure", "inheritance", "lexical", "scope"]},
        {"q": "Explain the concept of TDZ (Temporal Dead Zone) and how hosting differs between var, let, and const.", "keywords": ["tdz", "hoisting", "var", "let", "const"]},
        {"q": "Describe the differences between deep copying and shallow copying objects, and how structuredClone resolves reference nesting.", "keywords": ["shallow copy", "deep copy", "structuredclone", "reference", "mutation"]},
        {"q": "How does debouncing differ from throttling in client-side high-frequency event optimization?", "keywords": ["debounce", "throttle", "execution", "timer", "delay"]}
    ],
    "java": [
        {"q": "Describe JVM Memory management breakdown (Heap vs Stack) and how Garbage Collection tracking operates.", "keywords": ["jvm", "heap", "stack", "garbage collection", "generation"]},
        {"q": "Explain the behavioral difference between structural synchronization blocks and ReentrantLock APIs.", "keywords": ["synchronization", "reentrantlock", "thread", "lock", "fairness"]},
        {"q": "What is the collective purpose of Type Erasure in Java Generics at compile time?", "keywords": ["type erasure", "generics", "compile time", "bytecode", "backwards compatibility"]},
        {"q": "Contrast functional paradigms introduced via Java Streams against traditional imperative loops regarding pipeline evaluation.", "keywords": ["streams", "lazy evaluation", "terminal operation", "functional", "parallel"]},
        {"q": "Explain the design intent and memory structural safety of Java Records introduced in modern JDK specifications.", "keywords": ["records", "immutable", "final", "data transfer object", "constructor"]}
    ],
    "cpp": [
        {"q": "Detail resource allocation patterns using Resource Acquisition Is Initialization (RAII) and smart pointers.", "keywords": ["raii", "smart pointer", "unique_ptr", "shared_ptr", "destructor"]},
        {"q": "Explain virtual method tables (vtables) and how C++ resolves runtime polymorphism dynamically.", "keywords": ["vtable", "polymorphism", "virtual", "pointer", "runtime"]},
        {"q": "What is the difference between copy semantics and move semantics, and how does std::move optimize resource transitions?", "keywords": ["move semantics", "copy semantics", "std::move", "rvalue", "constructor"]},
        {"q": "Detail how undefined behavior risks emerge from dangling pointers, memory leaks, and buffer overflows.", "keywords": ["undefined behavior", "dangling pointer", "leak", "overflow", "pointer"]},
        {"q": "Explain template specialization and how C++ achieves compile-time template metaprogramming.", "keywords": ["template", "specialization", "metaprogramming", "compile-time", "generic"]}
    ],
    "golang": [
        {"q": "How do Go channels orchestrate thread-safe data synchronization without explicit mutex memory locks?", "keywords": ["channel", "goroutine", "synchronization", "csp", "block"]},
        {"q": "Explain the architectural model of the Go runtime scheduler pattern (M:N scheduler framework).", "keywords": ["scheduler", "goroutine", "work stealing", "machine", "processor"]},
        {"q": "How does Go approach error handling as values instead of using traditional try/catch exception flows?", "keywords": ["error handling", "defer", "panic", "recover", "multiple return"]},
        {"q": "Explain the internal structure of Go slices and how arrays back them during slice append allocations.", "keywords": ["slice", "underlying array", "capacity", "append", "allocation"]},
        {"q": "Detail structural composition in Go interfaces and how implicit satisfaction avoids explicit implements keywords.", "keywords": ["interface", "composition", "implicit", "duck typing", "struct"]}
    ],
    "ruby": [
        {"q": "Explain Ruby metaprogramming mechanics using method_missing and dynamically evaluated bindings.", "keywords": ["metaprogramming", "method_missing", "dynamic", "respond_to", "binding"]},
        {"q": "Contrast blocks, procs, and lambdas regarding scope encapsulation and return statement behaviors.", "keywords": ["proc", "lambda", "block", "return", "scope"]},
        {"q": "Explain the architectural flow of Ruby's method lookup path involving modules, mixins, and ancestors.", "keywords": ["method lookup", "ancestors", "mixin", "include", "prepend"]},
        {"q": "How does Ruby's Global VM Lock (GVL) impact concurrent vs parallel code execution threads?", "keywords": ["gvl", "thread", "concurrency", "parallelism", "mri"]},
        {"q": "Describe self-referential switching states of the 'self' keyword across object instance, class, and module blocks.", "keywords": ["self", "context", "receiver", "class method", "instance"]}
    ],
    "htmlcss": [
        {"q": "Analyze CSS stacking contexts and how BFCs (Block Formatting Contexts) isolate layout renderings.", "keywords": ["stacking", "z-index", "bfc", "layout", "isolation"]},
        {"q": "Contrast CSS Grid and Flexbox structural alignment paradigms for adaptive interface systems.", "keywords": ["grid", "flexbox", "axis", "dimension", "alignment"]},
        {"q": "Explain DOM tree construction, CSSOM pairing, and critical rendering path optimization to mitigate layout thrashing.", "keywords": ["critical rendering path", "dom", "cssom", "reflow", "repaint"]},
        {"q": "Detail semantic accessibility standards (WCAG) and how ARIA attributes support screen reader engines.", "keywords": ["aria", "accessibility", "wcag", "semantic", "screen reader"]},
        {"q": "Contrast structural usage and styling behavior of pseudo-classes vs pseudo-elements in CSS architecture.", "keywords": ["pseudo-class", "pseudo-element", "state", "content", "selectors"]}
    ],
    "react": [
        {"q": "Detail the continuous update reconciliation loop between the Virtual DOM and Fiber architectural nodes.", "keywords": ["virtual dom", "fiber", "reconciliation", "diffing", "render"]},
        {"q": "Analyze state tracking side-effects inside useEffect arrays and criteria forcing closure memory leaks.", "keywords": ["useeffect", "dependency", "cleanup", "closure", "leak"]},
        {"q": "Explain the performance design philosophy of React's Context API versus external stores like Redux for state propagation.", "keywords": ["context api", "redux", "state management", "rerender", "store"]},
        {"q": "How do React.memo, useMemo, and useCallback mitigate redundant child component evaluation trees?", "keywords": ["react.memo", "usememo", "usecallback", "memoization", "render"]},
        {"q": "Detail state preservation mechanisms across component unmount boundaries using key attributes during list reconciliation.", "keywords": ["key attribute", "unmount", "reconciliation", "identity", "state"]}
    ],
    "angular": [
        {"q": "How does Angular change detection strategy optimize performance utilizing Zone.js hooks?", "keywords": ["change detection", "zone", "onpush", "observable", "immutable"]},
        {"q": "Explain structural directives and dependency injection scoping hierarchies within lazy-loaded modules.", "keywords": ["directive", "injection", "module", "lazy", "provider"]},
        {"q": "Analyze the compilation architectural shifts between the legacy View Engine and Angular's modern Ivy pipeline.", "keywords": ["ivy", "view engine", "compilation", "tree shaking", "bundle"]},
        {"q": "Explain async multi-casting data flows utilizing RxJS Observables vs standard native Promises in services.", "keywords": ["rxjs", "observable", "stream", "operator", "subscription"]},
        {"q": "Detail structural protection models provided by Angular Route Guards (CanActivate, Resolve) for view orchestration.", "keywords": ["route guards", "canactivate", "resolve", "navigation", "interceptor"]}
    ],
    "datascience": [
        {"q": "Explain bias-variance trade-offs and structural implications of L1 Lasso vs L2 Ridge regularization.", "keywords": ["bias", "variance", "lasso", "ridge", "regularization"]},
        {"q": "Detail structural data parsing strategies handling extreme missingness or target vector class imbalance.", "keywords": ["imbalance", "smote", "imputation", "missing", "stratified"]},
        {"q": "Explain Principal Component Analysis (PCA) dimension reduction mechanics and preservation of variance vectors.", "keywords": ["pca", "eigenvalue", "dimensionality", "variance", "orthogonal"]},
        {"q": "Contrast evaluation metrics among Precision, Recall, F1-Score, and ROC-AUC for classification benchmarks.", "keywords": ["precision", "recall", "f1-score", "roc-auc", "confusion matrix"]},
        {"q": "Detail processing methodologies utilized in Time Series analysis to establish stationary distribution sequences.", "keywords": ["time series", "stationary", "arima", "seasonality", "autocorrelation"]}
    ],
    "machinelearning": [
        {"q": "Analyze structural optimization pathways minimizing loss using Stochastic Gradient Descent vs Adam optimizer.", "keywords": ["gradient", "sgd", "adam", "momentum", "learning rate"]},
        {"q": "Explain decision splits inside Random Forests and mathematical criteria (Gini vs Information Entropy).", "keywords": ["random forest", "gini", "entropy", "information gain", "split"]},
        {"q": "Describe Support Vector Machines hyper-plane convergence models and the mathematical role of Kernel Tricks.", "keywords": ["svm", "hyperplane", "kernel trick", "margin", "support vectors"]},
        {"q": "How does cross-validation mitigate model over-fitting during hyperparameter optimization phases?", "keywords": ["cross-validation", "k-fold", "overfitting", "hyperparameter", "validation"]},
        {"q": "Explain Ensemble Learning strategies, contrasting sequential Boosting architectures against parallel Bagging methods.", "keywords": ["boosting", "bagging", "ensemble", "xgboost", "random forest"]}
    ],
    "deeplearning": [
        {"q": "Detail internal structural calculations preventing vanishing gradients using ResNet skip connections.", "keywords": ["vanishing", "resnet", "skip connection", "residual", "backpropagation"]},
        {"q": "Explain the mathematical self-attention mechanism layout powering multi-headed transformer layers.", "keywords": ["attention", "transformer", "query", "key", "value"]},
        {"q": "Contrast structural mechanics of Convolutional Neural Networks (CNN) vs Recurrent Neural Networks (RNN) for sequence classification.", "keywords": ["cnn", "rnn", "spatial", "temporal", "lstm"]},
        {"q": "Detail how normalization protocols like Batch Normalization and Layer Normalization stabilize hidden distribution training layers.", "keywords": ["batch normalization", "layer normalization", "stabilize", "covariate shift", "activation"]},
        {"q": "Explain the target distribution optimization objectives of Generative Adversarial Networks (GANs) using minimax objective games.", "keywords": ["gan", "generator", "discriminator", "minimax", "latent space"]}
    ],
    "sql": [
        {"q": "Contrast structural transaction guarantees under ACID parameters against eventual consistency limits.", "keywords": ["acid", "consistency", "isolation", "transaction", "nosql"]},
        {"q": "Analyze structural optimization execution pathways using B-Tree index structures and query execution plans.", "keywords": ["index", "b-tree", "execution plan", "scan", "seek"]},
        {"q": "Explain isolating levels (Read Uncommitted through Serializable) and anomalies like Phantom Reads they mitigate.", "keywords": ["isolation level", "serializable", "phantom read", "dirty read", "locking"]},
        {"q": "Detail database scaling pathways, contrasting Master-Slave replication clustering against horizontal Sharding topologies.", "keywords": ["replication", "sharding", "horizontal scaling", "partitioning", "cluster"]},
        {"q": "How do write-ahead logging (WAL) loops preserve transactional durability across sudden infrastructure crashes?", "keywords": ["wal", "durability", "crash recovery", "buffer pool", "commit"]}
    ],
    "devops": [
        {"q": "Analyze file isolation primitives (Namespaces vs Cgroups) provisioning Linux container boundaries.", "keywords": ["namespace", "cgroups", "isolation", "container", "kernel"]},
        {"q": "Detail blue-green zero-downtime microservice architecture pathways compared to progressive canary updates.", "keywords": ["blue-green", "canary", "deployment", "traffic", "rollback"]},
        {"q": "Explain GitOps delivery architectures utilizing declarative state reconciliation via engines like ArgoCD.", "keywords": ["gitops", "argocd", "declarative", "reconciliation", "kubernetes"]},
        {"q": "Detail the integration boundaries of Infrastructure as Code (IaC) architectures managing state tracking maps using Terraform.", "keywords": ["terraform", "iac", "state file", "declarative", "provider"]},
        {"q": "Analyze centralized logging architectures, contrasting aggregate search engines like ELK Stack against Prometheus scraping matrices.", "keywords": ["elk", "prometheus", "metrics", "logs", "scraping"]}
    ],
    "cybersecurity": [
        {"q": "Analyze structural protection layout mechanisms distinguishing Symmetric (AES) and Asymmetric (RSA) encryption.", "keywords": ["symmetric", "asymmetric", "aes", "rsa", "public key"]},
        {"q": "Explain cross-site scripting (XSS) payload vectors and structural defense utilizing CSP constraints.", "keywords": ["xss", "csp", "sanitization", "injection", "script"]},
        {"q": "Detail the Zero Trust access security framework archetype and how it shifts network boundaries from perimeter models.", "keywords": ["zero trust", "least privilege", "iam", "perimeter", "authentication"]},
        {"q": "Explain how OAuth 2.0 authorization flows delegate API scoping access via JWT authorization tokens.", "keywords": ["oauth 2.0", "jwt", "token", "authorization", "scopes"]},
        {"q": "Analyze SQL Injection mitigation models, contrasting parameterized query statement bindings against blind sanitization scripts.", "keywords": ["sql injection", "parameterized", "prepared statement", "sanitization", "orm"]}
    ]
}

def evaluate_submission(user_answers, questions):
    review_data = []
    total_score = 0
    for i, item in enumerate(questions):
        ans = user_answers.get(f"answer_{i}", "").strip().lower()
        matched = [k for k in item["keywords"] if k.lower() in ans]
        missing = [k for k in item["keywords"] if k.lower() not in ans]
        q_score = int((len(matched) / len(item["keywords"])) * 100) if item["keywords"] else 0
        total_score += q_score
        review_data.append({
            "question": item["q"], "user_answer": user_answers.get(f"answer_{i}", ""),
            "matched": matched, "missing": missing, "score": q_score
        })
    final_score = int(total_score / len(questions)) if questions else 0
    if final_score >= 85: grade = "Principal Track Elite"
    elif final_score >= 70: grade = "Senior Associate Engineer"
    elif final_score >= 50: grade = "Associate Engineering Track"
    else: grade = "Needs Comprehensive Realignment"
    return final_score, grade, review_data

# --- ROUTES ---

@app.route('/')
@app.route('/home')
def home():
    return render_template('dashboard.html', step='home')

@app.route('/about')
def about():
    return render_template('dashboard.html', step='about')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email:
            session['user'] = email.split('@')[0].capitalize()
            session['history'] = []
            return redirect(url_for('dashboard'))
    return render_template('dashboard.html', step='login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email:
            session['user'] = email.split('@')[0].capitalize()
            session['history'] = []
            return redirect(url_for('dashboard'))
    return render_template('dashboard.html', step='signup')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('user'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'generate':
            skill = request.form.get('skill', 'python')
            level = request.form.get('level', 'fresher')
            questions = QUESTIONS_DB.get(skill, QUESTIONS_DB['python'])
            return render_template('dashboard.html', step='test', skill=skill, level=level, questions=questions)
            
        elif action == 'submit_answers':
            skill = request.form.get('skill', 'python')
            level = request.form.get('level', 'fresher')
            questions_list = QUESTIONS_DB.get(skill, QUESTIONS_DB['python'])
            
            total_score, performance_grade, review_data = evaluate_submission(request.form, questions_list)
            
            history_log = session.get('history', [])
            history_log.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "skill": skill, "level": level, "score": total_score
            })
            session['history'] = history_log
            return render_template('dashboard.html', step='review', total_score=total_score, performance_grade=performance_grade, review_data=review_data)

    return render_template('dashboard.html', step='setup', history=session.get('history', []))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)