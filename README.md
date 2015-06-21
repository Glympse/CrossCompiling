# Cross Compiling Console

## Introduction

Glympse Cross Compiling technology provides the ability to translate C++ code into Java and C#. The technology is heavily used at Glympse in a variety of client and server components. 

The easiest way to get an idea of how translation works is to play with online demo accessible at:
[http://demo.translator.dev.glympse.com/](http://demo.translator.dev.glympse.com/)

## Goals and Requirements

The need for the technology became obvious in early days of Glympse Client SDK (early 2012) when mobile OS market was already fragmented enough and web-based technologies were pretty much the only available option for implementing cross-platform applications. Being quite a vialbe option for application development it does not satisfy requirements applied to SDKs by application developers. The fact that most mobile applications are still written in native languages supported by OS vendors (iOS: Objective C/Swift, Android: Java, Windows Phone: C#, Blackberry: C++) still stands to this day (at least in social, business and utility applications). 

This led us to the idea of implementing cross-compiling technology allowing us to achieve the following goals: 
- Minimize investment into the development of truly cross-platform SDK (for mobile and desktop platforms).
- Provide consistent (identical whenever possible) public interface across all platforms. 
- Share documentation across all supported platforms. 
- Maintain portable, stable and performant code base.
  - Native, line to line identical code across all platforms (languages)
  - Efficient debugging / troubleshooting capabilities
  - Low cost of adoption of new platforms
- Ability to implement stack cross-platform components and implement portable multi-layered systems.
  - Unit tests / simulators / UI controls / extensions

Design process was wrapped around pretty strict requirements dictated mostly by goals outlined above:
- Support of the following programming languages:
  - C++ / Java / C#
- No sacrifices in performance! This requirement pretty much ruled out all scripting and VM-based techniques. 
- Code must be readable/debuggable across all platforms. It is of prime importance to have control over generated code even if it is not supposed to be modified.
- Native code (here and further down in this document 'native' does not necessarily refer to C++ but mostly means primary language supported by the OS. e.g. Java in Android world) should be executed on each platform. 
- The following components must be shared (written in common code):
  - Public interface
  - Business logic
  - Object model
  - Backend interaction (protocol, flow)
  - Persistence (local databases, configuration)
  - Resource handling.

## Approach

Code translation is essential part of the process. Common code is originally written in C++ and is translated into Java and C#.

A number of limitations are applied to the structure and syntax of the original code. Lowest common
denominator approach was used for selecting language features to be supported by the translator.

Platform-specific features and APIs are hidden by OS abstraction layer. Library remain functional if some features are not supported by a particular OS. Runtime detection is exposed by OSAL layer whenever necessary. 

<div align="center">
  <img width="75%" src="https://docs.google.com/drawings/d/1fGkXpYYSfgl9f0CvDgKKU09_5tMYpf4A7BIFXVSOXWo/pub?w=971&h=492">
</div>

## Memory Model

Object model management and memory model are fundamental blocks of any programming paradigm. Java and C# share the same (at least at concept level) approach to in-memory object representation, object allocation and lifecycle management. 

Explicit model defined by C++ can be adjusted to fit the model dictated by managed languages through the use of smart pointers. It is important to notice that there is a significant difference in the lifecycle of an object managed by a smart pointer or garbage collector. In the world where smart pointers are used object lifecycle is controlled exclusively by source code structure and scoping whereas background cleanup policies take complete control over object deallocation in managed environments. This can potentially cause differences in the performance of the same code running in different runtime, but at the same time it does not apply any limitations to code structure and syntax.

Smart pointer implementation provided as a part of translator's standard library uses both internal and external reference counting to get advantages of both worlds. As of now only strong pointers are supported which makes it application's responsibility to avoid reference loops of break those explicitly.

## Inheritance Model

Another important aspect of any object oriented system is inheritance model. Single inheritance is the only supported model of building relationships between classes. All interfaces on the system extend `ICommon` which is used as a basis for internal reference counting and powers other features natively exposed by Java's and C#'s Object class. 

This is an example diagram illustrating the use of the model:

<div align="center">
  <img width="50%" src="https://docs.google.com/drawings/d/1JgSL_3YvsBdmeaRQMjplvU3ocK6C38lVR83Gp_-jAOg/pub?w=932&h=378">
</div>

`Common<T>` helper was introduced to avoid implementing `ICommon` methods in all classes on the system. It only exists in C++ and is not translated to Java/C# where classes implement interfaces directly. 

The snippet below demonstrates basic use of interfaces and classes. 

```
class SomeClass : public AnotherClass, public Common< ISomeInterface > 
{
    public: struct IEntity : public ICommon
    {
        public: virtual bool evolve() = 0; 
    };
    /*C*/public: typedef O< IEntity > GEntity/**/

    private: GVector<GEntity>::ptr _entities;
    
    private: /*J*static**/ class Foo : public Common< IEntity >
    {
        public: virtual bool evolve()
        {
            // TODO: 
            return false;
        }
    };
    
    private: void test()
    {
        GEntity foo = new Foo();
        bool result = foo->evolve();
        
        for ( GEntiry entity : _entities )
        {
            entity->evolve();
        }
    }
    
    public: GEntity factory()
    {
        return new Foo();   
    }
};
```

You can see how this code is translated into Java/C# using online code converter tool mentioned above. 

## Adoption within Glympse

The technology found enormous amount of applications at Glympse. Here are examples of components implemented with the use of it:
Glympse Client SDK
- Glympse flagship platform shares 80k lines of common code across 5 topical mobile operating systems <br>
  (iOS, Android, Windows Phone, BlackBerry and Tizen). 
- JSON parser <br>
  Complete standard implementation with DOM and SAX models supported, flexible cancellation, error 
handling and, advanced performance optimization techniques. 
- WebSocket library (RFC 6455 compliant) <br>
  In-house implementation of one of the most popular real-time communication paradigms.
- RPC component <br>
  Transport layer built on top of Glympse Client SDK enabling interprocess communication capabilities 
heavily utilized in wearables and automotive applications. 
- API toolbox <br>
  Set of helpers and micro-libraries build on top of Client SDK as a demonstration of most common 
usage patterns. 
- Glympse Map control <br>
  Library powering Glympse viewing experience in native applications. Map control supports variety of 
rendering backends (including Apple MapKit, Google Map SDK, HERE Map SDK, 
WinPhone Map Control, Mapquest SDK) and shares business logic across all platforms. 
- Dispatch library <br>
  Component is designed to power B2C applications (aka Glympse EnRoute) built on top of 
Glympse Core. 	
- Unit Testing framework <br>
  Minimalistic library designed for efficient testing of client-side libraries exposing cross-platform API.
- Remote Debugger component <br>
  Debugging tool enabling remote monitoring of application object model.  

## References

Simple web application built on top of translating engine for demo/experimenting purposes. <br>
[https://github.com/Glympse/CrossCompilingConsole](https://github.com/Glympse/CrossCompilingConsole)

## License

Code is licensed under the [The MIT License](http://opensource.org/licenses/MIT). <br>
Documentation is licensed under [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Author

Cross Compiling technology was brought to life by Egor Pushkin. My recent efforts are targeted towards designing connected systems (mostly in mobile space) with focus on cross-platform development methodologies, modern communication paradigms and highly automated workflows.

LinkedIn - [https://www.linkedin.com/in/egorpushkin](https://www.linkedin.com/in/egorpushkin) <br>
Twitter - [https://twitter.com/egorpushkin](https://twitter.com/egorpushkin)
