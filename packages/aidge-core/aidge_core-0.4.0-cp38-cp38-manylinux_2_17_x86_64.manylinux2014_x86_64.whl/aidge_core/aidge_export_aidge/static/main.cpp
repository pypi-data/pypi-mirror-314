#include <iostream>
#include <aidge/backend/cpu.hpp>

/* Register default cpu Tensor implementation */
#include <aidge/backend/cpu/data/TensorImpl.hpp>

/* Include model generator */
#include "include/dnn.hpp"

int main()
{

    std::cout << "BEGIN" << std::endl;

    std::shared_ptr<Aidge::GraphView> graph = generateModel();

    std::cout << "END" << std::endl;

    return 0;
}
