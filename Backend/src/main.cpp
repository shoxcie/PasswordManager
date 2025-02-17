#define BOOST_PYTHON_STATIC_LIB
#include <boost/python.hpp>

#define OPENSSL_STATIC
#include <openssl/crypto.h>

#include <string>

namespace my_module
{
	int add(int const a, int const b)
	{
		return a + b;
	}

	std::string get_openssl_version()
	{
		const char* version = OpenSSL_version(OPENSSL_VERSION);
		if (version == nullptr) {
			throw std::runtime_error("Failed to get OpenSSL version");
		}

		return "OpenSSL version: " + std::string(OpenSSL_version(OPENSSL_VERSION));
	}
}

BOOST_PYTHON_MODULE(my_password_manager)
{
	using namespace boost::python;

	def("add", my_module::add);
	def("get_openssl_version", my_module::get_openssl_version);
}
