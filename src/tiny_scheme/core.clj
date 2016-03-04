(ns tiny-scheme.core
  (:gen-class))

(defn tagged-list?
  [exp symbol]
  (and (list? exp)
       (= (first exp) symbol)))

(defn lambda?
  [expr]
  (tagged-list? expr 'lambda))

(def built-in-functions
  {'+ +
   '- -
   '* *
   '/ /
   'mod mod})

(defn built-in-function?
  [expr]
  (not (nil? (get built-in-functions expr nil))))


(defn quoted?
  [expr]
  (tagged-list? expr 'quote))


(defn variable?
  [expr]
  (cond
   (symbol? expr) true
   :else false))

(defn define-function?
  [expr]
  (let [v (vec expr)
        [operator [fn-name & fn-params] & fn-body] v]
    (and (= operator 'define)
         (symbol? fn-name)
         (not (nil? fn-body)))))

(defn define-variable?
  [expr]
  (let [v (vec expr)
        [operator var-name value] v]
    (and (= operator 'define)
         (symbol? var-name)
         (not (nil? value)))))

(define assignment?
  [expr]
  (tagged-list? expr 'set!))

(defn test-repl
  []
  (let [expr (read)]
    (define-variable? expr)))

(test-repl)

(defn basic-element? 
  [expr]
  (cond
   (quoted? expr) true
   (number? expr) true
   (string? expr) true
   (built-in-function? expr) true
   :else false))


(def global-env (transient {}))

(defn user-defined-function?
  [fn-name]
  (nil? (get global-env fn-name nil)))

(defn make-function
  [fn-params fn-body]
  (list 'function fn-params fn-body))


(defn apply-built-in-function
  [fn args]
  (apply (get built-in-functions fn)
         args))

(defn eval-user-defined-function
  [fn-object env]
  (let [[_ fn-params fn-body] fn-object]
    (cond
     (last-expressoin? fn-body) (eval0 (first fn-body) env)
     :else (eval-user-defined-function
            (rest fn-body)
            env))))


(defn extend-env
  [keys values env]
  (cond
   (not= (count keys) (count values)) (throw (Exception. "args number unexpectred!"))
   :else (doseq [[k v] (map list keys values)]
                 (conj! env [k v]))))

(defn apply-user-defined-function
  [fn-name fn-args]
  (let [fn-object (get global-env fn-name)
        [_ fn-params _] fn-object
        extended-env (extend-env fn-params fn-args global-env)]
    (eval-user-defined-function fn-object extended-env)))


(defn apply0
  [fn args]
  (cond
   (built-in-function? fn) (apply-built-in-function fn args)
   (user-defined-function? fn) (apply-user-defined-function fn args)
   :else (throw (Exception. "Unkown function"))))

(defn eval0
  [expr env]
  (cond
   (basic-element? expr) expr
   (variable? expr) (get env expr)
   (define-function? expr) (let [[_ [fn-name & fn-params] & fn-body] (vec expr)]
                             (conj! env [fn-name (make-function fn-params fn-body)]))
   (define-variable? expr) (let [[_ var-name value] (vec expr)]
                             (conj! env [var-name (eval value env)]))
   :else (throw (Exception. "unsupport expression"))))

(defn repl
  []
  (print (str (ns-name *ns*) " >> "))
  (flush)
  (let [expr (read)
        env (transient {})
        value (eval0 expr env)]
    (when (not= value :quit)
      (println value)
      (recur))))


(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (repl))
