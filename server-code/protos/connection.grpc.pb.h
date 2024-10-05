// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: connection.proto
#ifndef GRPC_connection_2eproto__INCLUDED
#define GRPC_connection_2eproto__INCLUDED

#include "connection.pb.h"

#include <functional>
#include <grpc/impl/codegen/port_platform.h>
#include <grpcpp/impl/codegen/async_generic_service.h>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/client_context.h>
#include <grpcpp/impl/codegen/completion_queue.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/proto_utils.h>
#include <grpcpp/impl/codegen/rpc_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/status.h>
#include <grpcpp/impl/codegen/stub_options.h>
#include <grpcpp/impl/codegen/sync_stream.h>

class CreateWGConnection final {
 public:
  static constexpr char const* service_full_name() {
    return "CreateWGConnection";
  }
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    // creates the initial connection
    virtual ::grpc::Status StartConnection(::grpc::ClientContext* context, const ::ConnectionInit& request, ::ConnectionResp* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::ConnectionResp>> AsyncStartConnection(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::ConnectionResp>>(AsyncStartConnectionRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::ConnectionResp>> PrepareAsyncStartConnection(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::ConnectionResp>>(PrepareAsyncStartConnectionRaw(context, request, cq));
    }
    class experimental_async_interface {
     public:
      virtual ~experimental_async_interface() {}
      // creates the initial connection
      virtual void StartConnection(::grpc::ClientContext* context, const ::ConnectionInit* request, ::ConnectionResp* response, std::function<void(::grpc::Status)>) = 0;
      virtual void StartConnection(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::ConnectionResp* response, std::function<void(::grpc::Status)>) = 0;
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      virtual void StartConnection(::grpc::ClientContext* context, const ::ConnectionInit* request, ::ConnectionResp* response, ::grpc::ClientUnaryReactor* reactor) = 0;
      #else
      virtual void StartConnection(::grpc::ClientContext* context, const ::ConnectionInit* request, ::ConnectionResp* response, ::grpc::experimental::ClientUnaryReactor* reactor) = 0;
      #endif
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      virtual void StartConnection(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::ConnectionResp* response, ::grpc::ClientUnaryReactor* reactor) = 0;
      #else
      virtual void StartConnection(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::ConnectionResp* response, ::grpc::experimental::ClientUnaryReactor* reactor) = 0;
      #endif
    };
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    typedef class experimental_async_interface async_interface;
    #endif
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    async_interface* async() { return experimental_async(); }
    #endif
    virtual class experimental_async_interface* experimental_async() { return nullptr; }
  private:
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::ConnectionResp>* AsyncStartConnectionRaw(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::ConnectionResp>* PrepareAsyncStartConnectionRaw(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub final : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel);
    ::grpc::Status StartConnection(::grpc::ClientContext* context, const ::ConnectionInit& request, ::ConnectionResp* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::ConnectionResp>> AsyncStartConnection(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::ConnectionResp>>(AsyncStartConnectionRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::ConnectionResp>> PrepareAsyncStartConnection(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::ConnectionResp>>(PrepareAsyncStartConnectionRaw(context, request, cq));
    }
    class experimental_async final :
      public StubInterface::experimental_async_interface {
     public:
      void StartConnection(::grpc::ClientContext* context, const ::ConnectionInit* request, ::ConnectionResp* response, std::function<void(::grpc::Status)>) override;
      void StartConnection(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::ConnectionResp* response, std::function<void(::grpc::Status)>) override;
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      void StartConnection(::grpc::ClientContext* context, const ::ConnectionInit* request, ::ConnectionResp* response, ::grpc::ClientUnaryReactor* reactor) override;
      #else
      void StartConnection(::grpc::ClientContext* context, const ::ConnectionInit* request, ::ConnectionResp* response, ::grpc::experimental::ClientUnaryReactor* reactor) override;
      #endif
      #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      void StartConnection(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::ConnectionResp* response, ::grpc::ClientUnaryReactor* reactor) override;
      #else
      void StartConnection(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::ConnectionResp* response, ::grpc::experimental::ClientUnaryReactor* reactor) override;
      #endif
     private:
      friend class Stub;
      explicit experimental_async(Stub* stub): stub_(stub) { }
      Stub* stub() { return stub_; }
      Stub* stub_;
    };
    class experimental_async_interface* experimental_async() override { return &async_stub_; }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    class experimental_async async_stub_{this};
    ::grpc::ClientAsyncResponseReader< ::ConnectionResp>* AsyncStartConnectionRaw(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::ConnectionResp>* PrepareAsyncStartConnectionRaw(::grpc::ClientContext* context, const ::ConnectionInit& request, ::grpc::CompletionQueue* cq) override;
    const ::grpc::internal::RpcMethod rpcmethod_StartConnection_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    // creates the initial connection
    virtual ::grpc::Status StartConnection(::grpc::ServerContext* context, const ::ConnectionInit* request, ::ConnectionResp* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_StartConnection : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_StartConnection() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_StartConnection() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status StartConnection(::grpc::ServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestStartConnection(::grpc::ServerContext* context, ::ConnectionInit* request, ::grpc::ServerAsyncResponseWriter< ::ConnectionResp>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_StartConnection<Service > AsyncService;
  template <class BaseClass>
  class ExperimentalWithCallbackMethod_StartConnection : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    ExperimentalWithCallbackMethod_StartConnection() {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::Service::
    #else
      ::grpc::Service::experimental().
    #endif
        MarkMethodCallback(0,
          new ::grpc_impl::internal::CallbackUnaryHandler< ::ConnectionInit, ::ConnectionResp>(
            [this](
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
                   ::grpc::CallbackServerContext*
    #else
                   ::grpc::experimental::CallbackServerContext*
    #endif
                     context, const ::ConnectionInit* request, ::ConnectionResp* response) { return this->StartConnection(context, request, response); }));}
    void SetMessageAllocatorFor_StartConnection(
        ::grpc::experimental::MessageAllocator< ::ConnectionInit, ::ConnectionResp>* allocator) {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(0);
    #else
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::experimental().GetHandler(0);
    #endif
      static_cast<::grpc_impl::internal::CallbackUnaryHandler< ::ConnectionInit, ::ConnectionResp>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~ExperimentalWithCallbackMethod_StartConnection() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status StartConnection(::grpc::ServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    virtual ::grpc::ServerUnaryReactor* StartConnection(
      ::grpc::CallbackServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/)
    #else
    virtual ::grpc::experimental::ServerUnaryReactor* StartConnection(
      ::grpc::experimental::CallbackServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/)
    #endif
      { return nullptr; }
  };
  #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
  typedef ExperimentalWithCallbackMethod_StartConnection<Service > CallbackService;
  #endif

  typedef ExperimentalWithCallbackMethod_StartConnection<Service > ExperimentalCallbackService;
  template <class BaseClass>
  class WithGenericMethod_StartConnection : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_StartConnection() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_StartConnection() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status StartConnection(::grpc::ServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithRawMethod_StartConnection : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_StartConnection() {
      ::grpc::Service::MarkMethodRaw(0);
    }
    ~WithRawMethod_StartConnection() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status StartConnection(::grpc::ServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestStartConnection(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class ExperimentalWithRawCallbackMethod_StartConnection : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    ExperimentalWithRawCallbackMethod_StartConnection() {
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
      ::grpc::Service::
    #else
      ::grpc::Service::experimental().
    #endif
        MarkMethodRawCallback(0,
          new ::grpc_impl::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
                   ::grpc::CallbackServerContext*
    #else
                   ::grpc::experimental::CallbackServerContext*
    #endif
                     context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->StartConnection(context, request, response); }));
    }
    ~ExperimentalWithRawCallbackMethod_StartConnection() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status StartConnection(::grpc::ServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    #ifdef GRPC_CALLBACK_API_NONEXPERIMENTAL
    virtual ::grpc::ServerUnaryReactor* StartConnection(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)
    #else
    virtual ::grpc::experimental::ServerUnaryReactor* StartConnection(
      ::grpc::experimental::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)
    #endif
      { return nullptr; }
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_StartConnection : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_StartConnection() {
      ::grpc::Service::MarkMethodStreamed(0,
        new ::grpc::internal::StreamedUnaryHandler<
          ::ConnectionInit, ::ConnectionResp>(
            [this](::grpc_impl::ServerContext* context,
                   ::grpc_impl::ServerUnaryStreamer<
                     ::ConnectionInit, ::ConnectionResp>* streamer) {
                       return this->StreamedStartConnection(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_StartConnection() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status StartConnection(::grpc::ServerContext* /*context*/, const ::ConnectionInit* /*request*/, ::ConnectionResp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedStartConnection(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::ConnectionInit,::ConnectionResp>* server_unary_streamer) = 0;
  };
  typedef WithStreamedUnaryMethod_StartConnection<Service > StreamedUnaryService;
  typedef Service SplitStreamedService;
  typedef WithStreamedUnaryMethod_StartConnection<Service > StreamedService;
};


#endif  // GRPC_connection_2eproto__INCLUDED
